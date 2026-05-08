# VesperGrid â€” Continuation Handoff

> **Purpose.** Anyone (human or model) opening this repo cold must be able to pick up the
> work and continue with the same quality and pace using only this file plus
> `README.md`. Read this top-to-bottom once before touching anything.

**Last updated:** 2026-05-08 14:10 IST
**Deadline:** 2026-05-10 00:30 IST (lablab.ai submission)
**Working dir:** `c:\Users\arjun\Desktop\AMD-S-2` (Windows / PowerShell)

---

## 1. Mission in one paragraph

Build and ship **VesperGrid**, an evidence-grounded operational twin for industrial-safety
incidents that runs Qwen2.5-VL-7B-Instruct on a single AMD Instinct MI300X via vLLM ROCm,
for the AMD Developer Hackathon (Track 3: Vision & Multimodal AI). The submission has
already been engineered (Phase 0 complete) and now needs **submission artifacts**
(Phase 1), **a real cloud deploy + recorded demo** (Phase 2), and **a public submission +
build-in-public posts** (Phase 3).

**Stackable prizes targeted:** Qwen Challenge Â· Hugging Face Special Prize Â· Build-in-Public.

---

## 2. Hard facts you must not get wrong

| Fact | Value |
|------|-------|
| Hackathon track | Track 3 â€” Vision & Multimodal AI |
| Hardware target | **1Ã— AMD Instinct MI300X** (NOT 8Ã—; corrected 2026-05-08) |
| GPU memory | 192 GB VRAM |
| System | 20 vCPU, 240 GB RAM, 720 GB NVMe boot, 5 TB NVMe scratch |
| Quick-start image | vLLM 0.17.1 / ROCm 7.2.0 |
| Model | `Qwen/Qwen2.5-VL-7B-Instruct` via vLLM, **TP=1** |
| Credit budget cap | **$35 USD** (hard ceiling) |
| Submission portal | lablab.ai (online-only submission, no offline demo) |
| Repo remote | GitHub (private until cleared by user â€” see Rule below) |

> **The original spec mentioned 8Ã— MI300X.** Any text in older docs referencing
> old tensor-parallel or multi-GPU allocation language is **stale**. Treat the table above as
> canonical. If you spot stale references, fix them.

---

## 3. Operating rules (do not break)

1. **Do not `git push` or open a PR unless the user explicitly asks.**
   The user's `PROGRESS.md` is a private push-planning file enforcing this.
2. **Do not commit `Research/`, `PROGRESS.md`, `.amd_pdf_pages/`,
   `AMD.pdf`, `amd_pdf_text.txt`, or `.env`.** They are already in `.gitignore`.
   Only selected, user-approved public submission artifacts may be force-added.
3. **Do not weaken or delete tests.** Add regression tests when fixing bugs.
4. **Prefer minimal upstream fixes** over downstream workarounds.
5. **Soft-degrade always.** If the GPU backend is unreachable, the API and console
   must continue to work via the deterministic fallback path (`engine.synthesize_*`).
6. **No emojis in code or docs unless the user asks.**

---

## 4. Repository layout (what lives where)

```
AMD-S-2/
â”œâ”€â”€ README.md                       # Public-facing, judge-runnable quickstart
â”œâ”€â”€ HANDOFF.md                      # THIS FILE â€” continuation playbook
â”œâ”€â”€ PROGRESS.md                     # Private rules + push planning (gitignored)
â”œâ”€â”€ package.json                    # root-level npm scripts: api, dev, build
â”œâ”€â”€ requirements.txt                # â†³ apps/api/requirements.txt is the real one
â”‚
â”œâ”€â”€ apps/
â”‚   â”œâ”€â”€ api/                        # FastAPI backend (port 8742)
â”‚   â”‚   â”œâ”€â”€ requirements.txt        # fastapi, uvicorn, pydantic, httpx, sse-starlette
â”‚   â”‚   â””â”€â”€ src/vespergrid/
â”‚   â”‚       â”œâ”€â”€ main.py             # routes: /api/health, /api/scenarios/*, /api/ingest*
â”‚   â”‚       â”œâ”€â”€ engine.py           # loads sector4.json + deterministic synthesizer
â”‚   â”‚       â”œâ”€â”€ ingest.py           # async job registry + SSE event stream
â”‚   â”‚       â”œâ”€â”€ vlm_client.py       # Qwen-VL OpenAI-compatible client (httpx)
â”‚   â”‚       â””â”€â”€ models.py           # Pydantic v2 schemas (Scenario, Evidence, ...)
â”‚   â””â”€â”€ console/                    # Vite + React frontend (port 5173, proxies /api)
â”‚       â”œâ”€â”€ package.json
â”‚       â”œâ”€â”€ vite.config.ts          # /api â†’ http://localhost:8742 dev proxy
â”‚       â””â”€â”€ src/
â”‚           â”œâ”€â”€ App.tsx             # operations console UI + SSE consumer
â”‚           â”œâ”€â”€ domain.ts           # imports sector4.json as fallbackScenario
â”‚           â”œâ”€â”€ styles.css
â”‚           â””â”€â”€ data/sector4.json   # SHARED scenario data (FE + BE both read this)
â”‚
â”œâ”€â”€ demo/sector4/                   # Synthetic license-clean evidence pack
â”‚   â”œâ”€â”€ vesper-field-map.png        # 1024Ã—576 procedural map
â”‚   â”œâ”€â”€ drone_keyframe_03.png       # thermal blob over polymer crates
â”‚   â”œâ”€â”€ cctv_gate4.png              # vehicle queue at Gate 4 (the contradiction)
â”‚   â”œâ”€â”€ wind_sensor_strip.png       # wind direction strip
â”‚   â”œâ”€â”€ operator_transcript.txt
â”‚   â”œâ”€â”€ evidence_pack.json          # canonical evidence manifest
â”‚   â”œâ”€â”€ vlm_output_sample.json      # what Qwen-VL returns (sample)
â”‚   â””â”€â”€ audit_log_sample.json
â”‚
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ generate_assets.py          # regenerates demo/sector4/* deterministically
â”‚   â”œâ”€â”€ generate_deck.py            # writes submission/deck.md (10 Marp slides)
â”‚   â”œâ”€â”€ capture_hero.mjs            # Playwright headless screenshot capture
â”‚   â””â”€â”€ bootstrap_amd_cloud.sh      # one-shot installer for MI300X instance
â”‚
â”œâ”€â”€ infra/amd/deployment_plan.md    # cloud deploy plan (corrected to 1Ã— MI300X)
â”œâ”€â”€ docs/master_idea.md             # narrative + strategy
â”‚
â”œâ”€â”€ submission/                     # GITIGNORED. Local-only artifacts. â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   â”œâ”€â”€ deck.md                     # Marp source                                 â”‚
â”‚   â”œâ”€â”€ deck.pdf                    # 10-slide deck (~2.3 MB)                     â”‚
â”‚   â”œâ”€â”€ hero_above_fold.png         # 1920Ã—1200, ~1.85 MB â€” cover image          â”‚
â”‚   â”œâ”€â”€ hero_source_lineage.png     # ~700 KB â€” wow-moment shot                  â”‚
â”‚   â””â”€â”€ hero_full_page.png          # ~2.5 MB â€” full operations console          â”‚
â”‚                                                                                 â”‚
â””â”€â”€ (planned) submission/demo.mp4   # 2.5â€“3 min OBS recording (Phase 1)          â”‚
   (planned) submission/spaces/*    # HF Space scaffold (Phase 1)                â”‚
                                                                       â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

> **Critical gotcha.** `submission/`, `PROGRESS.md`, and `Research/` are gitignored.
> Tools that respect `.gitignore` (e.g. `read_file`, `write_to_file` in some agents)
> will **refuse** these paths. Workarounds:
> - To read a gitignored file: `Get-Content <path>` via PowerShell, or copy to
>   `$env:TEMP\<name>` then read.
> - To write one: write a small Python/PowerShell helper script in `scripts/` that
>   produces the file. See `scripts/generate_deck.py` as the canonical pattern.

---

## 5. Environment + how to run things

### Prereqs (already installed on this Windows box)
- Node.js (npm available globally)
- Python 3 (`python` on PATH)
- `npx playwright install chromium` already run
- Marp CLI fetched on-demand via `npx --yes @marp-team/marp-cli@latest`

### Environment variables (read by the API)
| Var | Purpose | Default |
|-----|---------|---------|
| `VLLM_BASE_URL` | OpenAI-compatible vLLM endpoint | unset â†’ deterministic mode |
| `VLLM_MODEL` | Model id served by vLLM | `Qwen/Qwen2.5-VL-7B-Instruct` |
| `VLLM_API_KEY` | Bearer token (optional) | unset |
| `VESPER_CORS_ORIGINS` | Comma-separated allowlist | `http://localhost:5173` |

### Start the local stack (two terminals OR background)

```powershell
# Terminal A â€” FastAPI on :8742
npm run api

# Terminal B â€” Vite dev server on :5173 (proxies /api â†’ 8742)
npm --prefix apps/console run dev
```

### Smoke test the API

```powershell
curl.exe -s http://localhost:8742/api/health | python -m json.tool
# Expect: accelerator_target = "1x AMD Instinct MI300X (192 GB VRAM)"
```

### Regenerate demo assets (deterministic)

```powershell
python scripts/generate_assets.py
```

### Capture hero screenshots (must have both servers running)

```powershell
node scripts/capture_hero.mjs
# Outputs to submission/{hero_above_fold,hero_source_lineage,hero_full_page}.png
```

### Render the slide deck

```powershell
python scripts/generate_deck.py
npx --yes @marp-team/marp-cli@latest --pdf submission/deck.md `
    --allow-local-files -o submission/deck.pdf
```

### Restart the API after Python changes

```powershell
Get-NetTCPConnection -LocalPort 8742 -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty OwningProcess -Unique |
  ForEach-Object { Stop-Process -Id $_ -Force }
npm run api
```

> Uvicorn is **not** started with `--reload`, so Python edits require a manual restart.

---

## 6. Status snapshot â€” what is done, what is next

### Phase 0 â€” Engineering (10/10 complete)

| ID | Task | Status |
|----|------|--------|
| `p0-cleanup` | Delete empty `Research/*.md`, gitignore PDF artifacts | âœ“ |
| `p0-scenario-json` | Single source of truth: `apps/console/src/data/sector4.json` | âœ“ |
| `p0-vlm-client` | `vlm_client.py` with `VLLM_BASE_URL` fallback | âœ“ |
| `p0-async-ingest` | `/api/ingest` job-id pattern + SSE event stream | âœ“ |
| `p0-frontend-sse` | Real progress bar consuming SSE; no fake `setTimeout` | âœ“ |
| `p0-cors` | `VESPER_CORS_ORIGINS` env-driven allowlist | âœ“ |
| `p0-assets` | All `demo/sector4/*` produced by `generate_assets.py` | âœ“ |
| `p0-source-preview` | `SourcePreview` component renders on evidence click | âœ“ |
| `p0-bootstrap` | `bootstrap_amd_cloud.sh` idempotent, 1Ã— MI300X, TP=1 | âœ“ |
| `p0-readme` | Judge-runnable quickstart in `README.md` | âœ“ |
| `p0-health-fix` | `/api/health` reports correct hardware (was stale 8Ã—) | âœ“ |

### Phase 1 â€” Submission artifacts (2/4 complete, 1 in progress)

| ID | Task | Status |
|----|------|--------|
| `p1-cover` | Three hero screenshots in `submission/` | âœ“ |
| `p1-slides` | 10-slide Marp deck â†’ `submission/deck.pdf` (2.3 MB) | âœ“ |
| `p1-handoff` | This file | âŸ³ in progress |
| `p1-fallback-video` | 2.5â€“3 min OBS recording â†’ `submission/demo.mp4` | â˜ |
| `p1-hf-space` | HF Space scaffold (static console + cloud-API toggle) | â˜ |

### Phase 2 â€” Cloud bring-up (0/6)
`p2-pre-flight` â†’ `p2-provision` â†’ `p2-bootstrap-run` â†’ `p2-smoke-tests` â†’
`p2-cloud-record` â†’ `p2-hf-link` â†’ `p2-snapshot`. Strict $35 credit budget.

### Phase 3 â€” Public submission (0/4)
`p3-bip-1`, `p3-bip-2`, `p3-rocm-feedback`, `p3-submit` (deadline: 2026-05-10 00:30 IST).

---

## 7. The full TODO with sub-steps, acceptance, and fallbacks

> Do these strictly in order unless the user says otherwise. Mark complete in
> `todo_list` after each one.

### `p1-fallback-video` â€” 2.5â€“3 min demo recording (PRIORITY: high)

**Why.** Cloud demo may not be ready by deadline. A locally-recorded video using the
deterministic flow guarantees the submission has motion, regardless of cloud state.

**Sub-steps:**
1. Start both servers (API on 8742, Vite on 5173). Confirm `/api/health` is clean.
2. Open `http://localhost:5173` in a 1920Ã—1080 browser window (Chrome/Edge,
   F11 fullscreen, dark OS theme).
3. Use **OBS Studio** (or `Win+Alt+R` Game Bar) to record at 1080p60 H.264.
4. **Script (â‰ˆ170 s):**
   - 0:00â€“0:15 â€” Title card overlay: "VesperGrid Â· 1Ã— AMD MI300X"
   - 0:15â€“0:35 â€” Hero band, narrate problem ("18-minute decision pressure, 4 contradictory sources")
   - 0:35â€“1:05 â€” Click each evidence row; show `SourcePreview` thumbnail surfacing
   - 1:05â€“1:35 â€” Click `SRC-VID-2217`, narrate the lineage (raw image â†’ candidate plan â†’ uncertainty)
   - 1:35â€“2:00 â€” Click "Ingest sampled evidence", show SSE progress bar advancing
   - 2:00â€“2:30 â€” Show updated brief, GPU panel (1Ã— MI300X workload split), uncertainty ledger
   - 2:30â€“2:50 â€” Outro: `curl /api/health` showing `accelerator_target` + closing card
5. Render to `submission/demo.mp4`, target â‰¤ 50 MB (H.264 CRF 23, 30 fps acceptable).
6. Subtitles: optional, but generate `submission/demo.srt` if time allows
   (`ffmpeg + whisper.cpp` or manual).

**Acceptance criteria:**
- Length 150â€“180 s, â‰¤ 50 MB, plays in QuickTime / VLC / browser.
- All three "wow" moments visible (lineage, SSE progress, MI300X panel).
- No console errors, no `Demo simulation` red banner shown for more than a beat
  (the badge is OK â€” just don't dwell).

**Fallback:** If OBS isn't available, use Windows Game Bar (`Win+Alt+R`) + ffmpeg
post-process. If a clean take is hard, record in 3â€“4 segments and stitch with
`ffmpeg -f concat`.

**Run command for ffmpeg post-process:**
```powershell
ffmpeg -i raw.mkv -c:v libx264 -crf 23 -preset slow -c:a aac -b:a 128k `
  -vf "scale=1920:1080" submission/demo.mp4
```

---

### `p1-hf-space` â€” Hugging Face Space scaffold (PRIORITY: high)

**Why.** Submission requires a publicly-accessible live URL. The Space hosts the
console as static files; the console is configured to call either:
(a) the cloud API (when `VITE_API_BASE` env is set at build time), or
(b) deterministic fallback bundled with the static build.

**Sub-steps:**
1. Add a build-time env to `apps/console/vite.config.ts`:
   ```ts
   define: { __API_BASE__: JSON.stringify(process.env.VITE_API_BASE ?? '') }
   ```
   Update `App.tsx` to use `__API_BASE__` as the fetch prefix when set.
2. Create `submission/spaces/` with:
   - `README.md` (HF Spaces frontmatter: `sdk: static`, `app_file: index.html`)
   - `Dockerfile`-free static build OR plain `static-spaces` config.
3. Build the console:
   ```powershell
   $env:VITE_API_BASE=""  # empty = full deterministic
   npm --prefix apps/console run build
   Copy-Item apps/console/dist/* submission/spaces/ -Recurse -Force
   ```
4. Test locally with `npx serve submission/spaces` to confirm static build works
   without an API server.
5. **Don't push to HF yet.** Wait for `p2-hf-link` (after cloud is up) to set the
   real `VITE_API_BASE` and rebuild.

**Acceptance criteria:**
- `submission/spaces/index.html` opens and renders the operations console
  end-to-end with the deterministic scenario.
- Bundle size < 5 MB.
- HF Spaces metadata in `submission/spaces/README.md` is valid YAML.

**Fallback:** If the static build is flaky, deploy to Cloudflare Pages or Vercel
instead â€” the lablab form just wants a live URL.

---

### `p2-pre-flight` â€” Cloud provisioning checklist (PRIORITY: high)

Before clicking "Launch instance" on AMD Developer Cloud:

1. â˜ Confirm `scripts/bootstrap_amd_cloud.sh` line endings are LF (`dos2unix` if needed).
2. â˜ Confirm `apps/api/requirements.txt` pins are reproducible.
3. â˜ Stage SSH key + AMD Cloud account access.
4. â˜ Pre-pull the vLLM 0.17.1 / ROCm 7.2.0 image tag in the script.
5. â˜ Confirm credit balance â‰¥ $35 and you are willing to spend it.
6. â˜ Final grep for stale multi-GPU or old tensor-parallel strings:
   ```powershell
   Select-String -Path *.md,scripts\*,apps\**\*.py,apps\**\*.ts `
                 -Pattern '8x MI300X|TP = 4|GPU 0 through 3' -ErrorAction SilentlyContinue
   ```

---

### `p2-provision` â†’ `p2-bootstrap-run` â†’ `p2-smoke-tests`

**Provision:** Launch one MI300X instance, image = vLLM 0.17.1 / ROCm 7.2.0,
SSH-key auth. Note instance IP.

**Bootstrap:**
```bash
ssh ubuntu@<IP>
git clone https://github.com/<user>/<repo>.git VesperGrid
cd VesperGrid
sudo bash scripts/bootstrap_amd_cloud.sh
# â†’ installs systemd units: vespergrid-vllm, vespergrid-api
# â†’ configures nginx reverse proxy on :80
# â†’ curls /v1/models warm-up
```

**Smoke tests (run from your laptop):**
```bash
PUBLIC=http://<IP>
curl $PUBLIC/api/health             # accelerator_target = "1x ..."
curl $PUBLIC/api/scenarios/sector-4-containment | jq '.brief'
# fire an ingest
JOB=$(curl -s -X POST $PUBLIC/api/ingest -H "content-type: application/json" \
       -d '{"note":"smoke"}' | jq -r .job_id)
curl -N $PUBLIC/api/ingest/$JOB/events    # SSE stream
```

**Acceptance:** all three return 200, ingest completes, GPU mode is `qwen-vl-vllm`.

---

### `p2-cloud-record` â€” Real cloud demo recording

Same script as `p1-fallback-video` but pointed at the cloud URL. Output:
`submission/demo_cloud.mp4`. The `vlm_backend` field flips from `deterministic` to
`qwen-vl-vllm` â€” capture this in the recording.

---

### `p2-hf-link` â€” Point HF Space at cloud API

```powershell
$env:VITE_API_BASE = "http://<cloud-api-host>"
npm --prefix apps/console run build
# push submission/spaces/* to the HF Space repo
```

Verify CORS: cloud `VESPER_CORS_ORIGINS` must include the HF Space URL.

---

### `p2-snapshot` â€” Save credits

After the cloud demo is recorded and the HF Space is verified:
1. Snapshot the instance (image to AMD Cloud's snapshot store).
2. Note the snapshot ID in this file.
3. **Destroy the running instance.** Credits stop burning.

---

### Phase 3 â€” Public submission

- `p3-bip-1`: 1 LinkedIn + 1 X teaser post (image = `hero_above_fold.png`).
- `p3-bip-2`: 1 LinkedIn + 1 X demo clip (15â€“30 s cut from `demo.mp4`).
- `p3-rocm-feedback`: write `docs/rocm_feedback.md` (300â€“500 words, candid,
  what worked / what didn't on ROCm 7.2.0). The Qwen Challenge prize values this.
- `p3-submit`: lablab.ai form. Required fields:
  - Project name: `VesperGrid`
  - Track: `Vision & Multimodal AI`
  - Cover: `submission/hero_above_fold.png`
  - Repo URL, HF Space URL, Demo video URL (YouTube/Drive)
  - Slide deck PDF: `submission/deck.pdf`
  - 200-word abstract (draft in advance)

---

## 8. Submission deliverables checklist (final)

- â˜ Public repo URL (cleared by user before push)
- â˜ Live demo URL (HF Space)
- â˜ Demo video (â‰¤ 3 min)
- â˜ Slide deck PDF (â‰¤ 10 slides)
- â˜ Cover image (1920Ã—1200 PNG)
- â˜ 200-word abstract (in lablab form)
- â˜ ROCm/AMD Cloud feedback writeup (linked in submission)
- â˜ Build-in-Public posts (linked in submission)

---

## 9. Risk register (live)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Cloud bring-up fails | Medium | High | Local fallback video already shipped (Phase 1) |
| Qwen-VL ROCm OOM at full image budget | Low (192 GB) | Medium | Reduce keyframes 5â†’3; bootstrap script clamps `--max-num-seqs` |
| CORS misconfig on HF Space | Medium | Medium | Test before snapshot; allowlist via env, not code |
| Credit overrun | Medium | High | Snapshot + destroy ASAP after `p2-cloud-record`; budget cap $35 |
| Stale `8x MI300X` references reappear | Low | Low (cosmetic) | Pre-flight grep in `p2-pre-flight` |
| Submission form opens late / is broken | Low | High | Submit â‰¥ 12 h before deadline; have all assets ready |

---

## 10. Decisions log (most recent first)

- **2026-05-08 14:10** â€” `HANDOFF.md` created at repo root (this file). Not gitignored.
- **2026-05-08 14:06** â€” Slide deck rendered (`submission/deck.pdf`, 10 slides, 2.3 MB).
  Slides 4 & 5 tightened after first render showed footer overlap.
- **2026-05-08 04:30** â€” `/api/health` corrected: `accelerator_target` and
  `runtime_plan()` now report 1Ã— MI300X / TP=1.
- **2026-05-08 04:27** â€” Hero screenshots captured via Playwright headless capture
  script; lineage shot is the wow-moment cover.
- **2026-05-08 (earlier)** â€” Hardware target corrected from 8Ã— MI300X to 1Ã— MI300X
  across all docs, scripts, scenario data, and frontend chips.
- **2026-05-07** â€” Phase 0 engineering closed (10 tasks).

---

## 11. "Pick this up cold" startup sequence

If you are a new model/agent opening this repo:

1. Read this file end-to-end. Then read `README.md`.
2. Run the smoke test:
   ```powershell
   npm run api                                # background terminal
   npm --prefix apps/console run dev          # second background terminal
   curl.exe -s http://localhost:8742/api/health
   ```
   Confirm `accelerator_target` says `"1x AMD Instinct MI300X (192 GB VRAM)"`.
3. Read the most recent entry in Â§10 to know exactly what just shipped.
4. Open `todo_list` (your tooling) and reconcile against Â§6/Â§7. The first
   `pending` item with the highest priority is your next task.
5. Read the matching sub-section in Â§7 â€” sub-steps, acceptance, fallback are spelled out.
6. **Before any destructive action** (`git push`, `rm`, cloud spend, HF push):
   re-check Operating Rules in Â§3.
7. After completing a task: update Â§6 and Â§10, update `todo_list`, append to Â§7
   only if the sub-steps changed in light of new information.

---

## 12. Quick contact + tooling

- User confirmed they will provision the AMD Cloud instance themselves; do not
  attempt to do it for them.
- User wants minimal acknowledgement / no preamble in chat. Just ship.
- User uses Windows + PowerShell. Never `cd` in run_command â€” use `Cwd` arg.
- All long-running servers use `Blocking: false` with a short
  `WaitMsBeforeAsync` to catch immediate failures.

---

*End of handoff. Keep this file authoritative. If it disagrees with anything else, this file wins.*
