"""VesperGrid HTTP surface.

Endpoints:
- GET  /api/health                              - liveness + runtime metadata
- GET  /api/scenarios/sector-4-containment      - deterministic scenario
- POST /api/ingest                              - kick off async pipeline (returns job_id)
- GET  /api/ingest/{job_id}                     - snapshot of job state
- GET  /api/ingest/{job_id}/events              - SSE event stream
- POST /api/ingest/{job_id}/await               - blocking convenience: await completion
                                                  (used by simple clients that cannot
                                                   consume SSE; kept short and bounded)
"""
from __future__ import annotations

import asyncio
import json
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from .engine import runtime_plan, sector_4_containment
from .ingest import IngestJob, registry, schedule
from .models import IngestRequest, Scenario

app = FastAPI(
    title="VesperGrid API",
    description="Multimodal evidence-to-simulation orchestration API for AMD MI300X deployments.",
    version="0.1.0",
)


def _allowed_origins() -> list[str]:
    raw = os.environ.get("VESPER_CORS_ORIGINS", "")
    if not raw:
        # Sensible local-dev default. Production deployments must set this
        # explicitly to the HF Space + cloud console origins.
        return [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    if raw.strip() == "*":
        return ["*"]
    return [o.strip() for o in raw.split(",") if o.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> dict[str, object]:
    return {
        "ok": True,
        "product": "VesperGrid",
        "track": "Vision & Multimodal AI",
        "positioning": "Critical Infrastructure Operational Twin",
        "accelerator_target": "1x AMD Instinct MI300X (192 GB VRAM)",
        "vlm_backend": "deterministic",
        "runtime_plan": runtime_plan(),
    }


@app.get("/api/scenarios/sector-4-containment", response_model=Scenario)
async def scenario() -> Scenario:
    return sector_4_containment()


@app.post("/api/ingest")
async def ingest(request: IngestRequest) -> dict:
    job = await registry.create(request)
    schedule(job)
    return {
        "job_id": job.id,
        "status": job.status,
        "backend": job.backend,
    }


def _require_job(job_id: str) -> IngestJob:
    job = registry.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job


@app.get("/api/ingest/{job_id}")
async def ingest_status(job_id: str) -> dict:
    return _require_job(job_id).snapshot()


@app.get("/api/ingest/{job_id}/events")
async def ingest_events(job_id: str, request: Request):
    job = _require_job(job_id)

    async def event_generator():
        async for ev in registry.stream(job):
            if await request.is_disconnected():
                break
            yield {
                "event": ev.stage,
                "id": str(ev.seq),
                "data": json.dumps(ev.to_dict()),
            }
        # Final frame so the client knows the stream is done and can read
        # the result snapshot in one hop.
        yield {
            "event": "snapshot",
            "data": json.dumps(job.snapshot()),
        }

    return EventSourceResponse(event_generator())


@app.post("/api/ingest/{job_id}/await")
async def ingest_await(job_id: str, timeout_seconds: float = 30.0) -> dict:
    """Blocking convenience for clients that cannot stream. Bounded so a
    stuck pipeline cannot deadlock a caller."""
    job = _require_job(job_id)
    deadline = asyncio.get_event_loop().time() + max(1.0, min(timeout_seconds, 120.0))
    while job.status not in ("complete", "failed"):
        if asyncio.get_event_loop().time() >= deadline:
            raise HTTPException(status_code=504, detail="job did not complete in time")
        await asyncio.sleep(0.1)
    return job.snapshot()
