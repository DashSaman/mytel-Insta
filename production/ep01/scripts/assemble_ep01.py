"""Assemble EP01_FINAL.mp4 from the six Flow clips.

Pipeline: scale/crop each clip to 1080x1920 @30fps -> hard cuts in story order ->
loudness-normalised native audio -> burned Persian subtitles (libass) -> small
official-logo badge -> short end card with the logo -> H.264/AAC MP4.

Usage:
  python -I assemble_ep01.py --clips <dir> --subs <file.ass> --fonts <dir>
      --logo-badge <png> --logo-big <png> --out <mp4>
      [--placeholders] [--endcard 1.6] [--max-clip 8.2]

--placeholders fills MISSING clips with clearly stamped test footage (pipeline
tests only; never for delivery).
"""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys

W, H, FPS = 1080, 1920, 30
CLIPS = [f"EP01_SH0{n}.mp4" for n in range(1, 7)]
NAVY = "0x061024"


def run(cmd: list[str], cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-4000:])
        raise SystemExit(f"command failed ({proc.returncode}): {cmd[0]}")
    return proc


def probe(path: pathlib.Path) -> dict:
    proc = run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    info = json.loads(proc.stdout)
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    return {
        "duration": float(info["format"]["duration"]),
        "width": int(video["width"]) if video else 0,
        "height": int(video["height"]) if video else 0,
        "has_audio": audio is not None,
        "fps": video.get("r_frame_rate") if video else None,
    }


def make_placeholder(target: pathlib.Path, label: str, seconds: float = 8.0) -> None:
    """Stamped test footage; generated inside the stage dir (cwd) so paths stay relative."""
    vf = (
        f"drawtext=fontfile=fonts/Vazirmatn-Bold.ttf:text='PLACEHOLDER {label} - NOT REAL FOOTAGE':"
        f"fontcolor=white:fontsize=44:box=1:boxcolor=black@0.7:boxborderw=16:x=(w-text_w)/2:y=(h-text_h)/2,format=yuv420p"
    )
    run(
        ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"testsrc2=size=360x640:rate={FPS}",
         "-f", "lavfi", "-i", "sine=frequency=330:sample_rate=48000", "-t", f"{seconds}", "-vf", vf,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "96k", "-shortest", target.name],
        cwd=target.parent,
    )


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", required=True)
    ap.add_argument("--subs", required=True)
    ap.add_argument("--fonts", required=True)
    ap.add_argument("--logo-badge", required=True)
    ap.add_argument("--logo-big", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--placeholders", action="store_true")
    ap.add_argument("--endcard", type=float, default=1.6)
    ap.add_argument("--max-clip", type=float, default=8.2)
    a = ap.parse_args()
    clips_dir, fonts_dir, out = pathlib.Path(a.clips), pathlib.Path(a.fonts), pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Stage inputs next to a temp working dir so FFmpeg filters can use plain relative paths.
    stage = out.parent / ".assemble_stage"
    if stage.exists():
        shutil.rmtree(stage)
    (stage / "fonts").mkdir(parents=True)
    for font in fonts_dir.glob("*.ttf"):
        shutil.copy2(font, stage / "fonts" / font.name)
    shutil.copy2(a.subs, stage / "subs.ass")
    shutil.copy2(a.logo_badge, stage / "badge.png")
    shutil.copy2(a.logo_big, stage / "logo_big.png")

    used, inputs, meta = [], [], []
    for i, name in enumerate(CLIPS):
        clip = clips_dir / name
        if not clip.exists() and a.placeholders:
            clip = stage / name
            make_placeholder(clip, name)
        if not clip.exists():
            raise SystemExit(f"missing clip: {clips_dir / name}")
        info = probe(clip)
        info["clip"] = str(clip)
        info["placeholder"] = clip.parent == stage
        meta.append(info)
        inputs += ["-i", str(clip)]
    durations = [min(m["duration"], a.max_clip) for m in meta]
    total = sum(durations)

    fc = []
    for i, d in enumerate(durations):
        v = f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={FPS},setsar=1"
        if meta[i]["height"] and meta[i]["height"] < 1000:
            v += ",unsharp=5:5:0.5:5:5:0.0"
        v += f",trim=duration={d:.3f},setpts=PTS-STARTPTS,format=yuv420p[v{i}]"
        fc.append(v)
        if meta[i]["has_audio"]:
            fc.append(f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=duration={d:.3f},asetpts=PTS-STARTPTS[a{i}]")
        else:
            fc.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f},asetpts=PTS-STARTPTS[a{i}]")
    fc.append("".join(f"[v{i}]" for i in range(6)) + "concat=n=6:v=1:a=0[vc]")
    fc.append("".join(f"[a{i}]" for i in range(6)) + "concat=n=6:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11[ac]")
    # Input indices: 0-5 clips, 6 end-card background, 7 logo badge, 8 big logo.
    bg, badge, big = 6, 7, 8
    fc.append(f"[{bg}:v]format=yuv420p[bg]")
    fc.append(f"[{big}:v]format=rgba,colorchannelmixer=aa=1,scale=820:-1:flags=lanczos[lgbig]")
    fc.append("[bg][lgbig]overlay=(W-w)/2:(H-h)/2:format=auto,format=yuv420p[endcard]")
    fc.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={a.endcard},asetpts=PTS-STARTPTS[sil]")
    fc.append("[vc][endcard]concat=n=2:v=1:a=0[vcat]")
    fc.append("[ac][sil]concat=n=2:v=0:a=1[acat]")
    fc.append("[vcat]ass=subs.ass:fontsdir=fonts,format=yuv420p[vsub]")
    fc.append(f"[{badge}:v]format=rgba,colorchannelmixer=aa=1,scale=236:-1:flags=lanczos[lg]")
    fc.append(f"[vsub][lg]overlay=64:250:enable='lt(t,{total - 0.15:.3f})':format=auto,format=yuv420p[vout]")

    cmd = ["ffmpeg", "-v", "error", "-y", *inputs]
    cmd += ["-f", "lavfi", "-i", f"color=c={NAVY}:s={W}x{H}:r={FPS}:d={a.endcard}"]
    cmd += ["-i", "badge.png", "-i", "logo_big.png"]
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[acat]"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS)]
    cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(out.resolve())]
    run(cmd, cwd=stage)
    final = probe(out)
    report = {
        "output": str(out),
        "clips": [{"file": m["clip"], "duration": m["duration"], "size": [m["width"], m["height"]], "placeholder": m["placeholder"]} for m in meta],
        "story_duration_s": round(total, 3),
        "endcard_s": a.endcard,
        "final_duration_s": final["duration"],
        "final_size": [final["width"], final["height"]],
        "final_fps": final["fps"],
        "final_has_audio": final["has_audio"],
        "any_placeholder": any(m["placeholder"] for m in meta),
    }
    out.with_suffix(".report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
