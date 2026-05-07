# VesperGrid

> **Critical infrastructure operational twin for AMD MI300X.** VesperGrid turns fragmented industrial evidence into a source-linked decision-support model that explains what is happening, what may happen next, and which candidate plan is safest under uncertainty.

**Hackathon track:** Vision & Multimodal AI
**Optional prize alignment:** Qwen Challenge, Hugging Face Special Prize, Build-in-Public

## Product Thesis

Industrial operators often receive scattered signals during high-pressure incidents: drone frames, fixed-camera footage, sensor readings, radio notes, and partial field reports. The hard part is not getting one more chatbot answer. The hard part is seeing which evidence supports which decision, where the uncertainty lives, and what action is safest under time pressure.

VesperGrid is designed as an **evidence-to-simulation console** for that moment. The demo scenario, **Sector 4 Solvent Containment**, is fully synthetic and fictional.

## AMD Cloud Target

This repository is being built around the corrected AMD Developer Cloud machine:

| Resource | Target |
|----------|--------|
| GPU | 1x AMD Instinct MI300X |
| GPU memory | 192 GB VRAM |
| CPU | 20 vCPU |
| System memory | 240 GB RAM |
| Boot disk | 720 GB NVMe |
| Scratch disk | 5 TB NVMe |
| Preferred quick-start | vLLM 0.17.1 + ROCm 7.2.0 |

The architecture assumes one large-memory MI300X, not an eight-GPU cluster. That makes the strategy sharper: keep one multimodal model warm, cap evidence batches carefully, stream progress to the UI, and use deterministic fallback paths for demo reliability.

## Planned Architecture

```text
synthetic evidence pack
  drone frame / CCTV still / sensor strip / operator note
              |
              v
       async ingest service
              |
      +-------+--------+
      |                |
 deterministic    Qwen-VL via vLLM
 fallback         on AMD MI300X
      |                |
      +-------+--------+
              |
              v
 source-linked operational twin
  evidence mesh / risk zones / candidate plan
  uncertainty ledger / runtime telemetry
              |
              v
 cinematic React operations console
```

## Repository Direction

The codebase is being pushed in deliberate, meaningful stages so the public history reads like a real product forming:

1. **Product foundation:** corrected identity, hardware target, README, progress tracker, basic app scaffolding.
2. **Scenario source of truth:** Sector 4 schema, typed scenario data, synthetic evidence manifest.
3. **Async ingest pipeline:** FastAPI job lifecycle, progress events, deterministic fallback.
4. **MI300X inference path:** vLLM-compatible Qwen-VL client and runtime configuration.
5. **Console experience:** cinematic evidence board, source lineage, uncertainty ledger, operator brief.
6. **Synthetic asset system:** procedural maps, sensor strips, CCTV/drone frames, audit samples.
7. **Deployment package:** AMD cloud bootstrap, Hugging Face Space strategy, demo readiness notes.

## Why This Is Different

VesperGrid is not a generic assistant and not a reskinned dashboard. Its core interaction is **source lineage**: a judge can click any recommended action and see the exact evidence item that shaped it. The system is intentionally honest about uncertainty instead of hiding ambiguity behind confident prose.

## License & Data

The planned license is **Apache-2.0**, which is friendly to open-source judging, demos, research reuse, and future startup commercialization.

All demo assets and scenario data are synthetic. No real facility footage, maps, CCTV, or private operational data should be committed.

## Project Status

The public repository is being developed through small, reviewable milestones. Internal progress notes and competition working logs are intentionally kept out of Git so the repo stays focused on source code, reproducible assets, deployment notes, and judge-facing documentation.
