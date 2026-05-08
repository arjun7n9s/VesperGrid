"""Async ingest job manager.

Solves the expert-review "synchronous trap": the UI must never block while
multimodal inference happens. Flow:

1. `POST /api/ingest`   -> creates job, returns {job_id, status:"queued"} immediately
2. background task     -> runs pipeline, emits events to a per-job queue
3. `GET  /api/ingest/{id}`         -> snapshot of current state (poll fallback)
4. `GET  /api/ingest/{id}/events`  -> SSE stream of stage events

This milestone runs deterministically so the UI behaves like the production
pipeline before the Qwen/vLLM PR lands. The next PR will swap the parsing
stage to a live VLM backend when `VLLM_BASE_URL` is configured.
"""
from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import AsyncIterator, Literal

from .engine import synthesize_from_ingest
from .models import IngestRequest, Scenario

JobStatus = Literal["queued", "running", "complete", "failed"]
EventStage = Literal[
    "queued",
    "sampling",
    "parsing",
    "normalizing",
    "synthesizing",
    "complete",
    "error",
]

# Sentinel pushed onto a job's queue to signal end-of-stream to SSE consumers.
_END_OF_STREAM = object()


@dataclass
class JobEvent:
    seq: int
    ts: float
    stage: EventStage
    message: str
    progress: float  # 0..1

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class IngestJob:
    id: str
    status: JobStatus
    request: IngestRequest
    events: list[JobEvent] = field(default_factory=list)
    result: Scenario | None = None
    error: str | None = None
    backend: Literal["deterministic"] = "deterministic"
    _queue: asyncio.Queue = field(default_factory=asyncio.Queue)

    def snapshot(self) -> dict:
        return {
            "job_id": self.id,
            "status": self.status,
            "backend": self.backend,
            "events": [e.to_dict() for e in self.events],
            "result": self.result.model_dump() if self.result else None,
            "error": self.error,
        }


class JobRegistry:
    """In-memory job registry. Adequate for hackathon scope; the demo is a
    single-tenant, single-incident scenario. Production would back this with
    Redis or DuckDB and add TTL-based eviction."""

    def __init__(self, max_jobs: int = 256) -> None:
        self._jobs: dict[str, IngestJob] = {}
        self._max_jobs = max_jobs
        self._lock = asyncio.Lock()

    async def create(self, request: IngestRequest) -> IngestJob:
        async with self._lock:
            if len(self._jobs) >= self._max_jobs:
                # FIFO eviction; the oldest finished job goes first.
                for jid, j in list(self._jobs.items()):
                    if j.status in ("complete", "failed"):
                        self._jobs.pop(jid, None)
                        break
            job = IngestJob(
                id=uuid.uuid4().hex[:12],
                status="queued",
                request=request,
                backend="deterministic",
            )
            self._jobs[job.id] = job
            return job

    def get(self, job_id: str) -> IngestJob | None:
        return self._jobs.get(job_id)

    async def emit(
        self,
        job: IngestJob,
        stage: EventStage,
        message: str,
        progress: float,
    ) -> None:
        ev = JobEvent(
            seq=len(job.events),
            ts=time.time(),
            stage=stage,
            message=message,
            progress=max(0.0, min(1.0, progress)),
        )
        job.events.append(ev)
        await job._queue.put(ev)

    async def close(self, job: IngestJob) -> None:
        await job._queue.put(_END_OF_STREAM)

    async def stream(self, job: IngestJob) -> AsyncIterator[JobEvent]:
        # Replay history first so latecomers see the full timeline.
        for ev in list(job.events):
            yield ev
        if job.status in ("complete", "failed"):
            return
        while True:
            item = await job._queue.get()
            if item is _END_OF_STREAM:
                return
            assert isinstance(item, JobEvent)
            yield item
            if item.stage in ("complete", "error"):
                return


registry = JobRegistry()


async def _run_pipeline(job: IngestJob) -> None:
    """Execute the multimodal pipeline. Stages are emitted as SSE events.

    The Qwen-VL handoff is intentionally deferred to the next PR. This keeps
    the async lifecycle reviewable on its own: queued, sampling, parsing,
    normalizing, synthesizing, complete.
    """
    job.status = "running"
    try:
        await registry.emit(job, "queued", "Job accepted by orchestrator.", 0.05)
        await asyncio.sleep(0)  # yield control

        # Stage 1: sampling (counts the evidence in the request)
        media_count = job.request.media_count
        sensor_count = job.request.sensor_count
        await registry.emit(
            job,
            "sampling",
            f"Sampling {media_count} media frames and {sensor_count} sensor traces.",
            0.20,
        )

        # Stage 2: deterministic parsing acknowledgement. The later VLM PR
        # will replace this block with live Qwen-VL parsing behind the same
        # event contract.
        await registry.emit(
            job,
            "parsing",
            "Using deterministic evidence parser; VLM handoff lands in the next milestone.",
            0.45,
        )

        # Stage 3: normalizing
        await registry.emit(
            job,
            "normalizing",
            "Normalizing observations into Entity / Location / Hazard / Constraint records.",
            0.75,
        )

        # Stage 4: synthesizing
        await registry.emit(
            job,
            "synthesizing",
            "Compiling source-linked candidate plan and uncertainty ledger.",
            0.90,
        )
        scenario = synthesize_from_ingest(job.request)
        job.result = scenario

        await registry.emit(
            job,
            "complete",
            f"Scenario ready with {len(scenario.evidence)} evidence items.",
            1.0,
        )
        job.status = "complete"
    except Exception as exc:  # pragma: no cover - last-ditch safety net
        job.status = "failed"
        job.error = str(exc)
        await registry.emit(job, "error", f"Pipeline failed: {exc}", 1.0)
    finally:
        await registry.close(job)


def schedule(job: IngestJob) -> asyncio.Task:
    """Detach the pipeline so the HTTP handler returns immediately."""
    return asyncio.create_task(_run_pipeline(job))
