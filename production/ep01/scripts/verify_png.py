"""Verify PNG files: signature, IHDR dimensions, SHA-256, and optional hash match.

Usage: python -I verify_png.py <file.png> [file2.png ...] --match <other_dir>
"""
import hashlib
import pathlib
import struct
import sys


def png_info(path: pathlib.Path) -> dict:
    data = path.read_bytes()
    out = {"file": path.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        out["valid_png"] = False
        return out
    width, height = struct.unpack(">II", data[16:24])
    out.update(
        valid_png=True,
        width=width,
        height=height,
        bit_depth=data[24],
        color_type=data[25],
    )
    # Walk chunks to make sure the file is complete (ends with IEND).
    pos = 8
    last = None
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        last = data[pos + 4 : pos + 8].decode("latin-1")
        pos += 12 + length
    out["ends_with_iend"] = last == "IEND" and pos == len(data)
    return out


def main(argv: list[str]) -> int:
    match_dir = None
    if "--match" in argv:
        i = argv.index("--match")
        match_dir = pathlib.Path(argv[i + 1])
        del argv[i : i + 2]
    bad = 0
    for arg in argv:
        p = pathlib.Path(arg)
        info = png_info(p)
        if match_dir is not None:
            other = match_dir / p.name
            if other.exists():
                same = hashlib.sha256(other.read_bytes()).hexdigest() == info["sha256"]
                info["matches_clone"] = same
                bad += 0 if same else 1
            else:
                info["matches_clone"] = "missing-in-clone"
        ok = info.get("valid_png") and info.get("ends_with_iend")
        bad += 0 if ok else 1
        print(("OK  " if ok else "BAD ") + " ".join(f"{k}={v}" for k, v in info.items()))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
