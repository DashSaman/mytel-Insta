# Episode 01 — Google Flow production

Status (2026-11-28): the reusable system is ready; the episode itself is **not generated yet**.

- Flow project (permanent, for all of Season 01): `MYTEL — SEASON 01 — MASTER PROJECT` — see [`../MYTEL_FLOW_ASSET_REGISTRY.json`](../MYTEL_FLOW_ASSET_REGISTRY.json) for the URL, the 7 characters, the 7 voices and the measured credit costs.
- `prompts/` — ready-to-paste prompts for the two environment plates and the six shots, written for the live Flow UI (`EP01_MASTER_PROMPT.md` is the step-by-step guide).
- `reports/` — what was verified, what is blocked and the exact next steps.
- `scripts/` — local pipeline: subtitles, 1080×1920 assembly with the official logo, voice check.
- `character_refs/` — the exact reference images uploaded to Flow (clean crops; the approved originals at the repository root are unchanged).
- `branding/` — official mytel.one logo files (downloaded from mytel.one) and the overlay derived from them.

To finish the episode: run the generations in Flow by hand (the service rejects automated generation), drop the clips in a `source_clips/` folder and run `scripts/make_subs.py` + `scripts/assemble_ep01.py`.
