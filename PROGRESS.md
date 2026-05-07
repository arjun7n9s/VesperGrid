# VesperGrid Progress

**Last updated:** 2026-05-08 04:24 IST
**Current goal:** Push 1 to GitHub as the clean public foundation for VesperGrid.
**Repository:** https://github.com/arjun7n9s/VesperGrid

## Current Direction

VesperGrid is a critical infrastructure operational twin for the AMD Developer Hackathon. The project is being rebuilt as an original product, separate from the earlier reference repo in name, architecture, UI philosophy, domain, and code organization.

The current product idea is **Sector 4 Solvent Containment**: a synthetic industrial safety scenario where drone frames, CCTV stills, sensor strips, and operator notes are converted into a source-linked operational picture.

The goal is not to build a generic AI chatbot. The judging moment should be:

1. A fragmented incident appears on screen.
2. The system ingests multimodal evidence.
3. The console generates a candidate action plan.
4. Every recommendation can be traced back to exact synthetic evidence.
5. The uncertainty ledger shows contradictions instead of pretending the answer is perfect.

## Competition Fit

**Primary track:** Vision & Multimodal AI
**Secondary alignment:** Qwen Challenge, Hugging Face Special Prize, Build-in-Public

Why this track fits:

- The demo depends on multimodal evidence, not text-only prompting.
- Qwen-VL via vLLM can be shown as the AMD MI300X inference path.
- The visual console gives judges something memorable to watch.
- Synthetic evidence avoids privacy and compliance issues.

## Correct AMD Cloud Specification

The selected AMD cloud machine is:

| Resource | Spec |
|----------|------|
| GPU | 1x AMD Instinct MI300X |
| VRAM | 192 GB |
| CPU | 20 vCPU |
| RAM | 240 GB |
| Boot disk | 720 GB NVMe |
| Scratch disk | 5 TB NVMe |
| Quick-start target | vLLM 0.17.1 + ROCm 7.2.0 |

Earlier planning mentioned an eight-GPU MI300X configuration. That assumption is now discarded. All public documentation and deployment design must target the single-GPU 192 GB MI300X machine.

## Push Strategy

We are not pushing the whole workspace at once. Each commit should show a meaningful product upgrade.

| Push | Theme | Status |
|------|-------|--------|
| 1 | Product foundation, corrected hardware target, public README, repo hygiene | in progress |
| 2 | Scenario source of truth and typed evidence schema | pending |
| 3 | Async ingest pipeline and deterministic fallback | pending |
| 4 | Qwen/vLLM integration path for MI300X | pending |
| 5 | Console redesign and source-lineage interaction | pending |
| 6 | Synthetic asset generation and demo evidence pack | pending |
| 7 | AMD cloud deployment and Hugging Face Space readiness | pending |
| 8 | Submission docs, pitch material, screenshots, and demo script | pending |

## Push 1 Scope

Push 1 should include only foundation files:

- README with VesperGrid identity and corrected AMD spec
- PROGRESS tracker with current direction and staged push plan
- `.gitignore` that protects research/raw artifacts and generated files
- package manifests and minimal app scaffolding
- API requirements and package marker
- corrected `Specs of Cloud.txt`
- GitHub push plan document if useful for public process transparency

Push 1 should not include:

- Research folder
- AMD.pdf
- generated submission assets
- local build output
- node_modules
- Python caches
- raw extracted PDF text

## Current Risks

| Risk | Concern | Response |
|------|---------|----------|
| Hardware mismatch | Docs or scripts accidentally assume 8 GPUs | Grep public files before each push |
| Overclaiming | Product sounds like full physics simulation | Describe MVP as evidence-linked decision support with bounded simulation |
| Demo fragility | Live model inference may be slow | Keep deterministic fallback and SSE progress states |
| Asset quality | Weak visuals reduce judge memory | Use strict synthetic asset selection and regenerate anything that looks cheap |
| Similarity risk | Original repo influence leaks into final project | Rename architecture, rebuild UX, avoid inherited workflows and terminology |

## Next Step After Push 1

Push 2 should focus on the scenario data model: one clean JSON source of truth, typed API/console contracts, and a small synthetic evidence manifest. That will make future inference, UI, and asset work cleaner.
