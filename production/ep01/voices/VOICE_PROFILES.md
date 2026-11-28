# MYTEL — permanent voice profiles (Google Flow custom voices)

Project: `MYTEL — SEASON 01 — MASTER PROJECT` — https://flow.google.com/project/9d5c55e4-b707-49b3-b852-77411ff81ec0

Each voice = a Flow preset (**Base**) + a **Customise performance** text. Never recreate or re-tune them between episodes.

| Voice | Base preset | Attached to | Sample dialogue (≤120 chars) | Preview |
|---|---|---|---|---|
| `MYTEL_AMIR_FA` | Puck (Male, upbeat, mid pitch) | Amir | ملیحه؟ خودتی؟ وای خدا، نکنه بابات گوشی رو برداره! | `MYTEL_AMIR_FA_preview.wav` (6.92 s) |
| `MYTEL_MALIHEH_FA` | Leda (Female, youthful, mid-high pitch) | Maliheh | بابا، صبر کن! اون تعمیرکار نیست! | `MYTEL_MALIHEH_FA_preview.wav` (4.16 s) |
| `MYTEL_NOSRATOLLAH_FA` | Algenib (Male, gravelly, low pitch) | Nosratollah | بله؟ کیه این وقت شب؟ آقا ما که کولر نداریم! | `MYTEL_NOSRATOLLAH_FA_preview.wav` (7.04 s) |
| `MYTEL_ZANGI_FA` | Sadachbia (Male, lively, low pitch) | Zangi | الو! باز عاشق‌ها افتادن به جون خط! | `MYTEL_ZANGI_FA_preview.wav` (3.88 s) |
| `MYTEL_SIMO_FA` | Fenrir (Male, excitable, younger pitch) | Simo | زنگی! باز شروع شد؟ من دیگه کشش ندارم! | `MYTEL_SIMO_FA_preview.wav` (6.00 s) |
| `MYTEL_DOKMEI_FA` | Kore (Female, firm, mid pitch) | Dokmei | ببین عزیزم، با این شماره گرفتنات تا فردا هم وصل نمی‌شی! | `MYTEL_DOKMEI_FA_preview.wav` (5.24 s) |
| `MYTEL_GHODRATI_FA` | Orus (Male, firm, mid-low pitch) | Ghodrati | داداش، دوران شما تموم شده! الان دیگه نوبت منه! | `MYTEL_GHODRATI_FA_preview.wav` (6.76 s) |

## Voice Performance text (exact)

### `MYTEL_AMIR_FA`

Native Iranian Persian (Farsi) speaker from Tehran. Young adult man, medium vocal pitch, warm and slightly youthful timbre. Natural conversational Tehran accent, emotionally expressive, charming, a little nervous, quick comedic reactions. Clear Persian pronunciation, natural breathing and pauses. Never robotic, never theatrical, never English-accented.

### `MYTEL_MALIHEH_FA`

Native Iranian Persian (Farsi) speaker from Tehran. Young adult woman, medium-high pitch, soft but confident vocal tone. Warm, intelligent, expressive, natural Tehran conversational accent. Gentle romantic delivery with believable comedic timing. Clear Persian pronunciation, natural breathing, no artificial squeaky voice. Never robotic, never theatrical, never English-accented.

### `MYTEL_NOSRATOLLAH_FA`

Native Iranian Persian (Farsi) speaker from Tehran. Older man in his late 50s, deep low-pitched baritone, mature slightly raspy vocal texture, authoritative traditional Iranian father. Slow deliberate speech, suspicious questioning, excellent deadpan comedy. Natural conversational Iranian Persian pronunciation, clear and intelligible. Never robotic, never theatrical, never English-accented.

### `MYTEL_ZANGI_FA`

Native Iranian Persian (Farsi) speaker from Tehran. Mature male cartoon character, slightly gravelly, medium-low pitch. Confident, talkative, nostalgic, expressive and humorous; a grumpy but lovable vintage rotary telephone. Strong comedic emphasis without exaggeration. Clear Persian pronunciation. Never robotic, never English-accented.

### `MYTEL_SIMO_FA`

Native Iranian Persian (Farsi) speaker from Tehran. Youthful male cartoon voice, higher pitch than a young adult man, energetic, mischievous, playful and slightly nasal. Quick delivery with clear articulation, elastic comedic personality. Never shrill, never unintelligible, never robotic, never English-accented.

### `MYTEL_DOKMEI_FA`

Native Iranian Persian (Farsi) speaker from Tehran. Mature woman, medium pitch, articulate, organized, intelligent, slightly sarcastic. Confident delivery with dry, precise comedic timing. Clear Persian pronunciation, natural pacing. Never robotic, never English-accented.

### `MYTEL_GHODRATI_FA`

Native Iranian Persian (Farsi) speaker from Tehran. Adult man, medium-low pitch, confident, showy, slightly arrogant, charismatic and humorous. Relaxed but expressive delivery, clear Persian pronunciation. Never robotic, never English-accented.


## Machine check

The previews were transcribed locally with faster-whisper (`medium`, language forced to `fa`). Every preview was detected as Persian with probability 1.00; token recall against the intended line is a rough indicator (the recogniser itself mis-hears colloquial words).

| Voice | Recall (medium) | Heard (medium) |
|---|---|---|
| `MYTEL_AMIR_FA` | 0.78 | ملیهه؟ خودتی؟ وای خدا نکنه بابا تک گوشی و بر داره |
| `MYTEL_MALIHEH_FA` | 0.67 | بابا سب کن. اون تمیر کار نیست. |
| `MYTEL_NOSRATOLLAH_FA` | 0.80 | بله؟ کیه این بخت شب؟ آقا ما که کولیر نداریم |
| `MYTEL_ZANGI_FA` | 0.57 | هلو؟ باز آشرا افتدن به جون خط |
| `MYTEL_SIMO_FA` | 0.88 | زنگی؟ با شروع شد؟ من دیگه کشش ندارم |
| `MYTEL_DOKMEI_FA` | 0.91 | ببین ازیزم، با این شماره گرفتنا تا فردا هم وصل نمیشی. |
| `MYTEL_GHODRATI_FA` | 0.89 | داداش دوران شما تموم شده الان دیگه نوبت منی |
