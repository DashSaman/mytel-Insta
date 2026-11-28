"""Write the production record files for EP01 from one data source.

Outputs (inside <ep01_dir>):
  MYTEL_FLOW_ASSET_REGISTRY.json, voices/VOICE_PROFILES.md,
  production/CREDIT_USAGE.csv, production/QUALITY_ASSURANCE.md,
  production/PRODUCTION_REPORT.md

No credentials are written. The account e-mail is deliberately omitted because
the registry is published to a public repository.

Usage: python -I write_registry.py <ep01_dir> <asr_json_medium> <asr_json_small>
"""
import json
import pathlib
import sys

PROJECT_ID = "9d5c55e4-b707-49b3-b852-77411ff81ec0"
PROJECT_URL = f"https://flow.google.com/project/{PROJECT_ID}"
GENERATED = "2026-11-28"

VOICES = {
    "MYTEL_AMIR_FA": ("Puck", "Male, upbeat, mid pitch", "ملیحه؟ خودتی؟ وای خدا، نکنه بابات گوشی رو برداره!", 6.92,
                      "Native Iranian Persian (Farsi) speaker from Tehran. Young adult man, medium vocal pitch, warm and slightly youthful timbre. Natural conversational Tehran accent, emotionally expressive, charming, a little nervous, quick comedic reactions. Clear Persian pronunciation, natural breathing and pauses. Never robotic, never theatrical, never English-accented."),
    "MYTEL_MALIHEH_FA": ("Leda", "Female, youthful, mid-high pitch", "بابا، صبر کن! اون تعمیرکار نیست!", 4.16,
                         "Native Iranian Persian (Farsi) speaker from Tehran. Young adult woman, medium-high pitch, soft but confident vocal tone. Warm, intelligent, expressive, natural Tehran conversational accent. Gentle romantic delivery with believable comedic timing. Clear Persian pronunciation, natural breathing, no artificial squeaky voice. Never robotic, never theatrical, never English-accented."),
    "MYTEL_NOSRATOLLAH_FA": ("Algenib", "Male, gravelly, low pitch", "بله؟ کیه این وقت شب؟ آقا ما که کولر نداریم!", 7.04,
                             "Native Iranian Persian (Farsi) speaker from Tehran. Older man in his late 50s, deep low-pitched baritone, mature slightly raspy vocal texture, authoritative traditional Iranian father. Slow deliberate speech, suspicious questioning, excellent deadpan comedy. Natural conversational Iranian Persian pronunciation, clear and intelligible. Never robotic, never theatrical, never English-accented."),
    "MYTEL_ZANGI_FA": ("Sadachbia", "Male, lively, low pitch", "الو! باز عاشق‌ها افتادن به جون خط!", 3.88,
                       "Native Iranian Persian (Farsi) speaker from Tehran. Mature male cartoon character, slightly gravelly, medium-low pitch. Confident, talkative, nostalgic, expressive and humorous; a grumpy but lovable vintage rotary telephone. Strong comedic emphasis without exaggeration. Clear Persian pronunciation. Never robotic, never English-accented."),
    "MYTEL_SIMO_FA": ("Fenrir", "Male, excitable, younger pitch", "زنگی! باز شروع شد؟ من دیگه کشش ندارم!", 6.0,
                      "Native Iranian Persian (Farsi) speaker from Tehran. Youthful male cartoon voice, higher pitch than a young adult man, energetic, mischievous, playful and slightly nasal. Quick delivery with clear articulation, elastic comedic personality. Never shrill, never unintelligible, never robotic, never English-accented."),
    "MYTEL_DOKMEI_FA": ("Kore", "Female, firm, mid pitch", "ببین عزیزم، با این شماره گرفتنات تا فردا هم وصل نمی‌شی!", 5.24,
                        "Native Iranian Persian (Farsi) speaker from Tehran. Mature woman, medium pitch, articulate, organized, intelligent, slightly sarcastic. Confident delivery with dry, precise comedic timing. Clear Persian pronunciation, natural pacing. Never robotic, never English-accented."),
    "MYTEL_GHODRATI_FA": ("Orus", "Male, firm, mid-low pitch", "داداش، دوران شما تموم شده! الان دیگه نوبت منه!", 6.76,
                          "Native Iranian Persian (Farsi) speaker from Tehran. Adult man, medium-low pitch, confident, showy, slightly arrogant, charismatic and humorous. Relaxed but expressive delivery, clear Persian pronunciation. Never robotic, never English-accented."),
}

CHARACTERS = [
    {"name": "Amir", "mention": "@Amir", "id": "1d489228-470a-4692-8a0d-9b9cd9912389", "source": "amir.png",
     "portrait": "amir_face.png", "portrait_px": [497, 861], "body": "amir_front.png", "body_px": [258, 969], "voice": "MYTEL_AMIR_FA", "kind": "human"},
    {"name": "Maliheh", "mention": "@Maliheh", "id": "df4c9c31-b19b-49e0-93d1-18404d3e724d", "source": "malihe.png",
     "portrait": "maliheh_face.png", "portrait_px": [438, 883], "body": "maliheh_front.png", "body_px": [250, 973], "voice": "MYTEL_MALIHEH_FA", "kind": "human"},
    {"name": "Nosratollah", "mention": "@Nosratollah", "id": "872f0c14-9748-43ef-9a59-df5e42ef2056", "source": "haj-nosratollah.png",
     "portrait": "nosratollah_head.png", "portrait_px": [268, 346], "body": "nosratollah_front.png", "body_px": [304, 600], "voice": "MYTEL_NOSRATOLLAH_FA", "kind": "human"},
    {"name": "Zangi", "mention": "@Zangi", "id": "3dbdd034-134f-474a-97c9-8b0e0afc0ae7", "source": "mr-zangi.png",
     "portrait": "zangi.png", "portrait_px": [768, 497], "body": None, "body_px": None, "voice": "MYTEL_ZANGI_FA", "kind": "object"},
    {"name": "Simo", "mention": "@Simo", "id": "2b76698b-8912-4901-9b31-0b21da2a4644", "source": "simo.png",
     "portrait": "simo.png", "portrait_px": [768, 484], "body": None, "body_px": None, "voice": "MYTEL_SIMO_FA", "kind": "object"},
    {"name": "Dokmei", "mention": "@Dokmei", "id": "36547dbb-9979-4f1b-864e-032fc827a072", "source": "mrs-dokmei.png",
     "portrait": "dokmei.png", "portrait_px": [760, 512], "body": None, "body_px": None, "voice": "MYTEL_DOKMEI_FA", "kind": "object"},
    {"name": "Ghodrati", "mention": "@Ghodrati", "id": "30439db3-8a14-407f-84d9-4c8d8714f61f", "source": "ghodrati.png",
     "portrait": "ghodrati.png", "portrait_px": [762, 512], "body": None, "body_px": None, "voice": "MYTEL_GHODRATI_FA", "kind": "object"},
]

SHOT_LINES = {
    1: [("Zangi", "الو! باز عاشق‌ها افتادن به جون خط!")],
    2: [("Amir", "ملیحه؟ خودتی؟")],
    3: [("Nosratollah", "بله؟ کیه این وقت شب؟")],
    4: [("Amir", "سلام، تعمیرکار کولرم! برای سرویس زنگ زدم.")],
    5: [("Nosratollah", "ما که کولر نداریم!"), ("Amir (offscreen, through the receiver)", "پس مشکل از همینه!")],
    6: [("Maliheh", "بابا... اون تعمیرکار نیست!")],
}
SHOT_REFS = {
    1: ["@Zangi", "@Simo", "LivingRoomNight"],
    2: ["@Amir", "AmirBedroomNight"],
    3: ["@Nosratollah", "LivingRoomNight"],
    4: ["@Amir", "AmirBedroomNight"],
    5: ["@Nosratollah", "LivingRoomNight"],
    6: ["@Nosratollah", "@Maliheh", "LivingRoomNight"],
}

BLOCK_MSG = "We noticed some unusual activity. Note that browser extensions that modify the page may cause issues. Please visit the Help Centre for more information. You have not been charged for this generation."


def load_asr(path: pathlib.Path) -> dict:
    if path.exists():
        return {r["voice"]: r for r in json.loads(path.read_text(encoding="utf-8"))["results"]}
    return {}


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    ep01 = pathlib.Path(argv[0])
    asr_m, asr_s = load_asr(pathlib.Path(argv[1])), load_asr(pathlib.Path(argv[2]))
    for c in CHARACTERS:
        c["url"] = f"{PROJECT_URL}/character/{c['id']}"
        c["voice_base_preset"] = VOICES[c["voice"]][0]
    voices = {}
    for name, (base, base_desc, sample, dur, perf) in VOICES.items():
        voices[name] = {
            "name": name, "mention_hint": f"@Voice: {name}", "base_preset": base, "base_preset_description": base_desc,
            "voice_performance": perf, "sample_dialogue": sample, "preview_file": f"voices/{name}_preview.wav",
            "preview_duration_s": dur, "preview_format": "WAV pcm_s16le 24000 Hz mono", "attached_to": [c["name"] for c in CHARACTERS if c["voice"] == name],
            "asr_medium": {k: asr_m.get(name, {}).get(k) for k in ("heard", "token_recall", "language", "language_probability")} if name in asr_m else None,
        }
    registry = {
        "schema": "mytel.flow-asset-registry/v1",
        "generated": GENERATED,
        "project": {
            "name": "MYTEL — SEASON 01 — MASTER PROJECT", "id": PROJECT_ID, "url": PROJECT_URL,
            "account": "personal Google account signed in to the in-app browser (e-mail intentionally omitted)",
            "purpose": "reusable for all 30 episodes; do not delete",
        },
        "generation_settings": {
            "mode": "Video", "video_type": "Ingredients", "model": "Omni 1.2 Flash", "aspect_ratio": "9:16",
            "resolution": {"720p": "3 credits per second", "360p": "1 credit per second"},
            "length_s": 8, "outputs": 1, "return_silent_videos": False, "visible_watermarking": False,
            "other_models_listed": ["Omni 1.1 Flash (leaving 5 Dec)", "Veo 3.1 - Lite", "Veo 3.1 - Fast (leaving 5 Dec)", "Veo 3.1 - Quality (leaving 5 Dec)"],
            "note": "Saved voices are only supported by the Omni Flash family in Ingredients mode.",
        },
        "credits": {"balance_at_check": 50, "checked": f"{GENERATED} (local time, before the failed generations)", "refresh": "daily at 16:31",
                    "consumed_this_run": 0, "episode_cost": {"6 x 8s @720p": 144, "6 x 8s @360p": 48, "images": 0}},
        "characters": CHARACTERS,
        "voices": list(voices.values()),
        "environments": [
            {"name": "LivingRoomNight", "intended_mention": "@LivingRoomNight", "status": "NOT generated", "prompt_file": "prompts/ENV_LivingRoomNight.txt"},
            {"name": "AmirBedroomNight", "intended_mention": "@AmirBedroomNight", "status": "NOT generated", "prompt_file": "prompts/ENV_AmirBedroomNight.txt"},
        ],
        "shots": [{"shot": n, "file": f"EP01_SH0{n}.mp4", "status": "NOT generated", "prompt_file": f"prompts/EP01_SH0{n}.txt",
                   "setup_file": f"prompts/EP01_SH0{n}.setup.txt", "references": SHOT_REFS[n], "lines": [{"speaker": s, "text": t} for s, t in SHOT_LINES[n]]} for n in range(1, 7)],
        "generation_ledger": [
            {"n": 1, "item": "LivingRoomNight image", "type": "image", "model": "Nano Banana 2.1", "settings": "9:16, x1", "attempts": 1, "credits": 0, "result": "rejected", "reason": BLOCK_MSG},
            {"n": 2, "item": "LivingRoomNight image (Retry button)", "type": "image", "model": "Nano Banana 2.1", "settings": "9:16, x1", "attempts": 1, "credits": 0, "result": "rejected", "reason": BLOCK_MSG},
            {"n": 3, "item": "7 custom voice previews", "type": "voice preview", "model": "Flow custom voice TTS", "settings": "base preset + performance", "attempts": 7, "credits": 0, "result": "accepted", "reason": ""},
            {"n": 4, "item": "EP01_SH01..SH06", "type": "video", "model": "Omni 1.2 Flash", "settings": "Ingredients, 9:16, 8s, x1", "attempts": 0, "credits": 0, "result": "not attempted", "reason": "generation blocked by the same safeguard; not retried on purpose"},
        ],
        "blocker": {
            "what": "Flow rejects generations started from the automated in-app browser",
            "message": BLOCK_MSG,
            "diagnosis": "no page hooks were active and browser functions were native; the embedded browser identifies itself as ZCode/Electron in its User-Agent",
            "policy": "the safeguard was not bypassed or masked; generation must be started by a person",
        },
        "local_pipeline": {
            "assemble": "python -I scripts/assemble_ep01.py --clips <dir> --subs EP01_SUBTITLES.ass --fonts fonts --logo-badge branding/mytel_logo_badge.png --logo-big branding/mytel_logo_transparent.png --out EP01_FINAL.mp4",
            "subtitles": "python -I scripts/make_subs.py production/EP01_CUES.draft.json <clips_dir> EP01_SUBTITLES.ass EP01_SUBTITLES.srt",
            "voice_check": "python scripts/asr_check.py voices production/voice_asr_check.json medium",
        },
    }
    (ep01 / "MYTEL_FLOW_ASSET_REGISTRY.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")

    rows = ["# MYTEL — permanent voice profiles (Google Flow custom voices)", "",
            f"Project: `MYTEL — SEASON 01 — MASTER PROJECT` — {PROJECT_URL}", "",
            "Each voice = a Flow preset (**Base**) + a **Customise performance** text. Never recreate or re-tune them between episodes.", "",
            "| Voice | Base preset | Attached to | Sample dialogue (≤120 chars) | Preview |", "|---|---|---|---|---|"]
    for name, (base, desc, sample, dur, _perf) in VOICES.items():
        rows.append(f"| `{name}` | {base} ({desc}) | {voices[name]['attached_to'][0]} | {sample} | `{name}_preview.wav` ({dur:.2f} s) |")
    rows += ["", "## Voice Performance text (exact)", ""]
    for name, (_base, _desc, _sample, _dur, perf) in VOICES.items():
        rows += [f"### `{name}`", "", perf, ""]
    rows += ["", "## Machine check", "",
             "The previews were transcribed locally with faster-whisper (`medium`, language forced to `fa`). Every preview was detected as Persian with probability 1.00; "
             "token recall against the intended line is a rough indicator (the recogniser itself mis-hears colloquial words).", "",
             "| Voice | Recall (medium) | Heard (medium) |", "|---|---|---|"]
    for name in VOICES:
        r = asr_m.get(name)
        rows.append(f"| `{name}` | {r['token_recall']:.2f} | {r['heard']} |" if r else f"| `{name}` | n/a | |")
    (ep01 / "voices" / "VOICE_PROFILES.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

    csv = ["n,item,type,model,settings,attempts,credits,accepted,rejected,reason",
           "1,LivingRoomNight image,image,Nano Banana 2.1,9:16 x1,1,0,0,1,\"unusual activity (not charged)\"",
           "2,LivingRoomNight image retry,image,Nano Banana 2.1,9:16 x1,1,0,0,1,\"unusual activity (not charged)\"",
           "3,Custom voice previews,voice preview,Flow custom voice TTS,base preset + performance,7,0,7,0,",
           "4,EP01_SH01..SH06,video,Omni 1.2 Flash,\"Ingredients, 9:16, 8s, x1\",0,0,0,0,not attempted (safeguard)",
           ",TOTAL,,,,9,0,7,2,"]
    (ep01 / "production" / "CREDIT_USAGE.csv").write_text("\n".join(csv) + "\n", encoding="utf-8")
    print("registry, voice profiles and ledger written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
