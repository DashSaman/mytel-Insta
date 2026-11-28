# EP01 — الو... فوت نکن! | Flow production guide (verified against the live UI)

Status: characters, voices and the master project are **done and saved in Flow**. Environment plates and the six
clips are **not generated yet**: Flow rejected automated generation with
`We noticed some unusual activity … browser extensions that modify the page may cause issues` (nothing was charged).
Every generation below has to be started by a person (see "How to run a generation").

## Project
- Flow project: `MYTEL — SEASON 01 — MASTER PROJECT`
- URL: https://flow.google.com/project/9d5c55e4-b707-49b3-b852-77411ff81ec0
- Account: open the link with the Google account that owns the project (the account signed in on the production PC).

## Generation settings (prompt box → settings)
| Setting | Value |
|---|---|
| Mode | Video |
| Video type | Ingredients (required: voice references only work in Ingredients) |
| Model | Omni 1.2 Flash (the only family that supports saved voices) |
| Aspect ratio | 9:16 |
| Resolution | 720p (3 credits/sec) or 360p (1 credit/sec) |
| Length | 8 sec |
| Output count | x1 |
| Project → Settings → Return silent videos | OFF (verified) |
| Account → Visible watermarking | OFF (verified) |

Credit facts measured in the account on 2026-11-28: balance **50 credits**, refreshes daily at 16:31.
720p = 3 credits/sec (8 s → 24), 360p = 1 credit/sec (8 s → 8). Images (Nano Banana 2.1) = 0 credits.
Six 8-second clips cost 144 credits at 720p or 48 credits at 360p.

## Master prompt prefix (prepend to every shot)
```text
High-quality cinematic stylized 3D animated Iranian comedy, authentic late-1990s setting, vertical 9:16. Preserve the exact registered identity, facial proportions, clothing, colours, materials and voice of every attached character. Natural character animation, expressive acting, convincing comedic timing, warm cinematic lighting, correct anatomy, stable geometry. Generate native synchronized audio. The spoken dialogue is exactly the Persian text given in quotation marks, in natural Iranian Persian (Tehran accent), spoken only by the named speaker; only the speaking character moves their mouth, every other character stays silent and reacts naturally. No narrator, no extra dialogue, no translated dialogue, no music overpowering speech, no invented characters, no face morphing, no duplicate objects, no extra limbs, no modern technology, no on-screen text and no subtitles.
```

## Dialogue (exact, do not edit)
| Shot | Speaker | Line |
|---|---|---|
| SH01 | Zangi | الو! باز عاشق‌ها افتادن به جون خط! |
| SH02 | Amir | ملیحه؟ خودتی؟ |
| SH03 | Nosratollah | بله؟ کیه این وقت شب؟ |
| SH04 | Amir | سلام، تعمیرکار کولرم! برای سرویس زنگ زدم. |
| SH05 | Nosratollah → Amir (offscreen, through the receiver) | ما که کولر نداریم! → پس مشکل از همینه! |
| SH06 | Maliheh | بابا... اون تعمیرکار نیست! |

## How to run a generation
1. Open the project, type `@` in the prompt box and pick the character from the autocomplete list (a real chip must
   appear; plain text names are not references).
2. Add the environment plate with `+ Add ingredients` → pick the image from the project.
3. Paste the shot prompt, check the settings table, press Generate once and wait for it to finish.
4. Start with **SHOT 03**. Keep it if it passes the checks below, then generate SH01, SH02, SH04, SH05, SH06.
5. Download each clip (hover → More → Download) and name it `EP01_SH0n.mp4`.

## Checks before the next generation
Correct character identity · same face as the reference · correct room · masculine/feminine voice matches the
character · natural Iranian Persian · exact dialogue · lips move only for the speaker · stable animation · 9:16.

## Notes learned from the live UI
- A character can hold 1 or 2 images: **Portrait** (face) and **Body** (full figure). Humans have both; the four
  telephone characters have one full-figure image.
- Voices are project assets. Custom voices are made from a preset + "Customise performance" and attached with
  "Add to character". Clicking a voice in a **filtered** (searched) list attaches the preset directly — clear the
  search box first.
- In shots where a human holds the telephone, do **not** attach `@Zangi`: describe it as an ordinary mustard-yellow
  rotary telephone (no face, no eyes, no limbs). Humans never see or hear the living objects.
