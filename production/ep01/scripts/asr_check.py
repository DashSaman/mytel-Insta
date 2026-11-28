"""Machine check of the Flow voice previews with local speech recognition.

Transcribes each preview WAV with faster-whisper (Persian) and compares it with
the expected line using normalised token recall. Nothing leaves the machine.

Usage: python asr_check.py <voices_dir> <out_json> [model]
"""
import json
import pathlib
import re
import sys

EXPECTED = {
    "MYTEL_AMIR_FA": "ملیحه؟ خودتی؟ وای خدا، نکنه بابات گوشی رو برداره!",
    "MYTEL_MALIHEH_FA": "بابا، صبر کن! اون تعمیرکار نیست!",
    "MYTEL_NOSRATOLLAH_FA": "بله؟ کیه این وقت شب؟ آقا ما که کولر نداریم!",
    "MYTEL_ZANGI_FA": "الو! باز عاشق‌ها افتادن به جون خط!",
    "MYTEL_SIMO_FA": "زنگی! باز شروع شد؟ من دیگه کشش ندارم!",
    "MYTEL_DOKMEI_FA": "ببین عزیزم، با این شماره گرفتنات تا فردا هم وصل نمی‌شی!",
    "MYTEL_GHODRATI_FA": "داداش، دوران شما تموم شده! الان دیگه نوبت منه!",
}

DIACRITICS = re.compile(r"[\u064B-\u065F\u0670\u200C\u200F\u200E]")
PUNCT = re.compile(r"[^\w\s\u0600-\u06FF]", re.UNICODE)


def normalise(text: str) -> list[str]:
    text = DIACRITICS.sub("", text)
    text = text.replace("ي", "ی").replace("ك", "ک").replace("ۀ", "ه").replace("ة", "ه")
    text = PUNCT.sub(" ", text)
    return [t for t in text.split() if t]


def recall(expected: list[str], heard: list[str]) -> float:
    if not expected:
        return 0.0
    pool = list(heard)
    hit = 0
    for w in expected:
        # Accept the stem (Persian clitics such as "می‌شی" may be split by the model).
        for i, h in enumerate(pool):
            if h == w or (len(w) > 3 and (h.startswith(w[:4]) or w.startswith(h[:4]))):
                hit += 1
                del pool[i]
                break
    return hit / len(expected)


def load_audio(path: pathlib.Path, rate: int = 16000) -> "object":
    """Decode any audio to mono float32 at `rate` with FFmpeg (avoids the PyAV API mismatch)."""
    import subprocess

    import numpy as np

    pcm = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(rate), "-f", "s16le", "-"],
        check=True,
        capture_output=True,
    ).stdout
    return np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    voices_dir, out_json = pathlib.Path(argv[0]), pathlib.Path(argv[1])
    model_name = argv[2] if len(argv) > 2 else "small"
    from faster_whisper import WhisperModel

    model = None
    for candidate in (model_name, "base"):
        try:
            model = WhisperModel(candidate, device="cpu", compute_type="int8")
            model_name = candidate
            break
        except Exception as exc:  # download or load failure -> try the smaller model
            print(f"model {candidate} failed: {str(exc)[:160]}", flush=True)
    if model is None:
        print("no ASR model could be loaded")
        return 2
    results = []
    for name, expected_text in EXPECTED.items():
        wav = voices_dir / f"{name}_preview.wav"
        if not wav.exists():
            results.append({"voice": name, "error": "preview file missing"})
            continue
        audio = load_audio(wav)
        segments, info = model.transcribe(audio, language="fa", beam_size=5, vad_filter=False)
        heard = " ".join(s.text.strip() for s in segments).strip()
        exp, got = normalise(expected_text), normalise(heard)
        results.append(
            {
                "voice": name,
                "expected": expected_text,
                "heard": heard,
                "token_recall": round(recall(exp, got), 3),
                "language": info.language,
                "language_probability": round(info.language_probability, 3),
                "duration_s": round(info.duration, 2),
            }
        )
        r = results[-1]
        print(f"{name:24s} recall={r['token_recall']:.2f} lang={r['language']}({r['language_probability']:.2f})  heard: {heard}", flush=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps({"model": model_name, "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
