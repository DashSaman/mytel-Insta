"""Build the EP01 subtitles (ASS for burn-in + SRT sidecar) from a cue list.

Cue times are relative to the start of their own clip, so the result follows the
real duration of the clips found in <clips_dir>.

Usage: python -I make_subs.py <cues.json> <clips_dir> <out_ass> <out_srt>
"""
import json
import pathlib
import subprocess
import sys

CLIPS = [f"EP01_SH0{n}.mp4" for n in range(1, 7)]
STYLE = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{size},&H00FFFFFF,&H00FFFFFF,&H50000000,&H60000000,-1,0,0,0,100,100,0,0,1,5,0,2,110,110,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def duration(path: pathlib.Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out)


def ass_time(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def srt_time(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s, ms = s + 1, 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    cues_path, clips_dir, out_ass, out_srt = (pathlib.Path(a) for a in argv[:4])
    spec = json.loads(cues_path.read_text(encoding="utf-8"))
    starts = {}
    cursor = 0.0
    for name in CLIPS:
        clip = clips_dir / name
        starts[name] = cursor
        cursor += duration(clip) if clip.exists() else 8.0
    events = []
    for cue in spec["cues"]:
        clip = CLIPS[cue["shot"] - 1]
        base = starts[clip]
        text = cue["text"].strip()
        events.append((base + float(cue["start"]), base + float(cue["end"]), text, cue.get("style", "Default")))
    style = spec.get("style", {})
    header = STYLE.format(font=style.get("font", "Vazirmatn"), size=style.get("font_size", 60), margin_v=style.get("margin_v", 640))
    out_ass.parent.mkdir(parents=True, exist_ok=True)
    out_ass.write_text(
        # U+200F (right-to-left mark) forces an RTL paragraph, so a line that starts
        # with "(" or another neutral character keeps its Persian punctuation order.
        header + "".join(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},{st},,0,0,0,,\u200f{text}\n" for a, b, text, st in events),
        encoding="utf-8",
    )
    out_srt.write_text(
        "".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{text}\n\n" for i, (a, b, text, _st) in enumerate(events, 1)),
        encoding="utf-8",
    )
    print(f"total clips duration: {cursor:.3f}s, cues: {len(events)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
