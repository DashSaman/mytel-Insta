# EP01 — Quality assurance record

Date: 2026-11-28. Every line states what was actually checked; nothing below is assumed.

## A. Source assets
| Check | Result | Evidence |
|---|---|---|
| 7 approved PNGs downloaded from the repository `main` | PASS | valid PNG signatures, complete IEND, SHA-256 identical to the git clone |
| Characters match the character bible | PASS | visual review of all 7 images (colours, clothing, telephone objects) |
| Original PNGs unchanged | PASS | only read; crops are separate files in `characters/refs/` |
| Reference views free of text / neighbour figures | PASS | crops reviewed at zoom; the Nosratollah name label sits in open background and was repainted with the surrounding background colour (no figure pixel touched) |

## B. Google Flow project
| Check | Result | Evidence |
|---|---|---|
| Permanent project exists and is named | PASS | `MYTEL — SEASON 01 — MASTER PROJECT` |
| 7 permanent characters saved | PASS | re-opened after a full page reload: name, portrait, body (humans), info text present for all 7 |
| 7 custom voices attached | PASS | each character shows its `MYTEL_*_FA` voice; all 7 appear in the "Add ingredients" list with their voice |
| Character `@` autocomplete | PARTIAL | characters are listed as selectable prompt assets; the `@` popup itself could not be seen because the in-app browser pane had stopped rendering |
| Return silent videos = OFF | PASS | project Settings, aria-checked=false |
| Visible watermarking = OFF | PASS | account panel, aria-checked=false |
| Collections (CHARACTERS, ENVIRONMENTS, …) | NOT DONE | skipped: creation needs drag-and-drop or the Flow Agent; nothing was organised |

## C. Voices
| Check | Result | Evidence |
|---|---|---|
| 7 previews exported | PASS | WAV, 24 kHz mono, 3.88–7.04 s, normal speech level (≈ −25 dB mean, −1.5 dB peak) |
| Previews are Persian | PASS | local speech recognition (faster-whisper medium, forced `fa`): language probability 1.00 for all 7 |
| Previews match the intended line | PASS (rough) | token recall 0.57–0.91; the recogniser itself mis-hears colloquial words |
| Pronunciation / accent by ear | NOT VERIFIED | the agent cannot listen; a human must approve the 7 preview files |
| Lip synchronisation, voice inside video | NOT VERIFIED | no clip exists yet |

Watch items from the transcripts (possible weak words, check in the real clips): Zangi «عاشق‌ها» (heard "آشرا"),
Maliheh «صبر کن» (heard "سب کن"), Nosratollah «وقت شب» (heard "بخت شب"). If a clip mispronounces one of them,
add minimal diacritics to that word in the video prompt (subtitles keep standard spelling).

## D. Environments and clips
| Item | Result |
|---|---|
| LivingRoomNight, AmirBedroomNight | NOT generated — Flow rejected the request (anti-automation safeguard), twice, not charged |
| EP01_SH01 … EP01_SH06 | NOT generated — not attempted on purpose: same safeguard, no bypass |

## E. Editing pipeline (tested with stamped placeholder footage only)
| Check | Result | Evidence |
|---|---|---|
| End-to-end render | PASS | `_qa/pipeline_test/EP01_PIPELINE_TEST.mp4`: 1080×1920, 30 fps, 49.6 s (48 s story + 1.6 s end card), H.264/AAC |
| Persian subtitles | PASS | Vazirmatn Bold, right-to-left order and letter joining verified on all 7 lines; RTL mark added so punctuation stays correct |
| Subtitle position | PASS | centred, baseline ≈ 66 % of the height, clear of the Reels top bar and bottom caption zone |
| Official logo | PASS | small navy badge top-left for the story, large logo on the end card; artwork taken unchanged from mytel.one (background made transparent) |
| Audio | PASS | loudness-normalised to −14 LUFS, true peak −9.5 dBTP on the test tone |
| Real cue timing | PENDING | `production/EP01_CUES.draft.json` holds estimated times; re-time from the real clip audio |

## F. Final deliverables
| Deliverable | Status |
|---|---|
| `EP01_FINAL.mp4` | NOT produced (no clips) |
| `MYTEL_EP01_COMPLETE.zip` | NOT produced (would be incomplete); a production pack with the real files exists instead |
| `MYTEL_FLOW_ASSET_REGISTRY.json` | produced, no credentials |
