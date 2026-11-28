# EP01 — Production report (الو... فوت نکن!)

Date: 2026-11-28 · Episode not finished: the reusable production system is built; generation is blocked and needs a person to press Generate.

## Outcome in one paragraph
The permanent Flow project, all seven characters (with reference images) and seven permanent Persian voices are saved and verified.
Prompts, the editing pipeline, subtitles and the official logo overlay are ready and tested. Flow refused to generate from the
automated browser with an anti-automation error ("We noticed some unusual activity…", nothing charged), so the two environment
plates and the six clips do not exist yet and `EP01_FINAL.mp4` was not rendered.

## What was done, in order
1. Read the repository (README, EP01, character map, bible, asset manifest, Flow workflow) and the live official Flow docs.
2. Downloaded the 7 approved images from `main`, verified format and hashes, reviewed them visually.
3. Extracted clean reference views (portrait + full body for the three humans; full figure for the four telephone characters).
4. Created and named the Flow project; verified "Return silent videos" and "Visible watermarking" are off.
5. Registered 7 characters (name, portrait, body, character info) and 7 custom voices; reloaded the page and re-read every field.
6. Measured credit costs, built the prompts, the assembly pipeline, subtitles and logo assets; tested the pipeline with placeholders.
7. Ran local speech recognition on the voice previews as an objective check.
8. Attempted the first environment image → rejected; used the tile's own Retry once → rejected again; stopped there.

## Decisions
- **New project instead of reuse.** The existing "Boogh-e Eteshal - mytel.one" project holds other characters (Boss, Poya, Negin…), not this series.
- **Portrait + body.** The live UI allows 1–2 images per character; humans got the face close-up as Portrait and the full figure as Body.
- **No AI body generation.** "Create body" would have spent credits and redrawn approved designs; approved images were uploaded instead.
- **No `@Zangi` in human shots.** The telephone a person holds is an ordinary phone (no face, no limbs); the prompt says so explicitly.
- **Credits.** Balance 50 (refreshes daily 16:31). 720p = 3 credits/s, 360p = 1 credit/s. Six 8-second clips cost 144 (720p) or 48 (360p). Images are free.
- **Safeguard not bypassed.** Flow's anti-automation check rejects generations started from the automated embedded browser (it identifies itself as ZCode/Electron); the block was respected.

## Changes made outside this folder (for transparency)
- **Flow account:** one new project, 7 characters, 7 voices. In that project: "Show tile details" switched on, prompt-box settings left on
  Image / 9:16 / x1, and one failed image tile (LivingRoomNight) left in place with Retry/Delete buttons. Other projects were only viewed.
- **In-app browser:** the tab that showed the Google sign-in page was navigated to flow.google.com and is now a second Flow tab.
- **This PC:** an isolated Python environment at `mytel-ep01/.venv` (speech recognition) and its two Whisper models
  (about 2 GB) in the user's Hugging Face cache folder. Nothing was installed globally and no system setting was changed.
  A temporary local file server (127.0.0.1:8765) was used for uploads/downloads and has been stopped.

## Next steps
1. Open https://flow.google.com/project/9d5c55e4-b707-49b3-b852-77411ff81ec0 in a normal browser with the same Google account
   (or bring the ZCode window to the front and use its browser pane).
2. Follow `prompts/EP01_MASTER_PROMPT.md`: generate the two environment images (free) and name them `LivingRoomNight` and
   `AmirBedroomNight`; generate **SHOT 03** first, check it, then SH01, SH02, SH04, SH05, SH06. Start with 360p for a complete
   draft today (48 credits) or 720p for quality (24 credits per clip).
3. Download the clips as `EP01_SH01.mp4` … `EP01_SH06.mp4` into `source_clips/`.
4. Run the QA on the real clips (dialogue by speech recognition, speaker/lip check on frames, cue re-timing), then:
   `python -I scripts/make_subs.py production/EP01_CUES.draft.json source_clips EP01_SUBTITLES.ass EP01_SUBTITLES.srt`
   `python -I scripts/assemble_ep01.py --clips source_clips --subs EP01_SUBTITLES.ass --fonts fonts --logo-badge branding/mytel_logo_badge.png --logo-big branding/mytel_logo_transparent.png --out EP01_FINAL.mp4`
5. Build `MYTEL_EP01_COMPLETE.zip` and publish the backup.

## Known limitations
- Pronunciation quality was checked by machine transcription only, not by ear.
- The `@` autocomplete popup was not seen on screen (browser pane was not rendering at that moment).
- Collections in Flow were not created.
- Cue timings are estimates until real clips exist.
