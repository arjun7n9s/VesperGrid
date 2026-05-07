"""Scenario engine.

The deterministic Sector 4 scenario lives in a single JSON file shared with
the React console (`apps/console/src/data/sector4.json`). This module loads
that JSON, validates it through Pydantic, and applies bounded mutations for
the live-ingest path. When `VLLM_BASE_URL` is set the ingest path delegates
to the Qwen-VL client; otherwise it falls back to deterministic synthesis so
the demo remains reproducible even with no GPU backend.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .models import (
    EvidenceItem,
    IngestRequest,
    Scenario,
    UncertaintyIssue,
)

# engine.py -> vespergrid -> src -> api -> apps -> console/src/data/sector4.json
_SCENARIO_PATH = (
    Path(__file__).resolve().parents[3]
    / "console"
    / "src"
    / "data"
    / "sector4.json"
)


@lru_cache(maxsize=1)
def _load_sector4() -> dict:
    if not _SCENARIO_PATH.exists():
        raise FileNotFoundError(
            f"Sector 4 scenario JSON not found at {_SCENARIO_PATH}. "
            "Frontend and API share this file; do not delete it."
        )
    return json.loads(_SCENARIO_PATH.read_text(encoding="utf-8"))


def sector_4_containment() -> Scenario:
    """Return a fresh Pydantic-validated copy of the deterministic scenario."""
    return Scenario.model_validate(_load_sector4())


def synthesize_from_ingest(request: IngestRequest) -> Scenario:
    """Deterministic synthesis used when no live VLM backend is configured.

    Bounded transformation: nudges confidence based on evidence pressure and
    appends a source-linked operator note + uncertainty if field notes were
    provided. Real model integration lives in `vlm_client.py` and is invoked
    by the async ingest path in `main.py` when `VLLM_BASE_URL` is set.
    """
    base = sector_4_containment()
    evidence_pressure = min(
        0.08,
        (request.media_count * 0.009) + (request.sensor_count * 0.002),
    )
    base.location = request.location
    base.confidence = min(0.94, base.confidence + evidence_pressure)

    field_note = request.field_notes.strip()
    if field_note:
        base.evidence.append(
            EvidenceItem(
                id="ev-live-notes",
                sourceUuid="SRC-LIVE-9001",
                source="Live operator note",
                kind="report",
                summary=field_note[:220],
                confidence=0.71,
                signal="human context",
                linkedZoneId="z3",
            )
        )
        base.uncertainties.append(
            UncertaintyIssue(
                id="u-live",
                kind="missing_data",
                title="Live note needs verification",
                detail=(
                    "The newest operator note was preserved, but VesperGrid "
                    "has not yet received confirming imagery."
                ),
                severity="watch",
                sourceEntityIds=["SRC-LIVE-9001"],
            )
        )
        base.brief.append(
            "Live operator note was added as a source-linked graph observation."
        )
    return base


def runtime_plan() -> list[str]:
    return [
        "Serve Qwen-VL through vLLM ROCm on a single MI300X (TP=1, 192 GB VRAM).",
        "Sample up to five keyframes per clip and submit them as a single multi-image request.",
        "Normalize model outputs into Entity, Location, Hazard, and Constraint records with strict Pydantic validation.",
        "Keep graph/vector state in 240 GB system RAM for the demo; flush asynchronously to the 5 TB scratch NVMe.",
        "Run the simulation layer as CPU/vectorized MVP while GPU-resident multimodal inference demonstrates MI300X value.",
    ]
