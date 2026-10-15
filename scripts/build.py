#!/usr/bin/env python3
"""Single-resume build entrypoint.

Builds the current resume in latestresume/ plus the generic template,
auto-detecting an optional headshot for the final PDF.

Flow: latestresume/ holds ONLY the current resume. When it is superseded,
move the old version to "My resumes - old/" for reference and put the new
version in latestresume/.

Photo convention (shared by all targets):
    assets/photo.jpg | assets/photo.jpeg | assets/photo.png
    - First file found (in that order) is embedded top-right.
    - No photo -> headers fall back to a clean centered layout.

Usage (from repo root):
    python3 scripts/build.py              # current resume (default)
    python3 scripts/build.py --template   # generic public template (smoke test)
    python3 scripts/build.py --all        # everything

Outputs land in output/pdf/ (gitignored).
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output" / "pdf"

PHOTO_CANDIDATES = ["assets/photo.jpg", "assets/photo.jpeg", "assets/photo.png"]

TARGETS = {
    "resume": "latestresume/AdityaSharma_230958070_CSFT.tex",
    "template": "templates/resume.tex",
}


def find_photo() -> Path | None:
    for candidate in PHOTO_CANDIDATES:
        p = ROOT / candidate
        if p.is_file():
            return p
    return None


def run(cmd: list[str]) -> None:
    print(f"+ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(f"Command failed ({result.returncode}): {' '.join(cmd)}")


def build_tex(name: str) -> Path:
    tex = ROOT / TARGETS[name]
    if not tex.is_file():
        raise SystemExit(f"Missing source: {tex}")
    if shutil.which("tectonic") is None:
        raise SystemExit("tectonic not found on PATH. Install it: https://tectonic-typesetting.github.io/")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    photo = find_photo()
    print(f"[{name}] photo: {photo.relative_to(ROOT) if photo else 'none (centered header)'}")

    run(["tectonic", "-o", str(OUTPUT_DIR), str(tex)])
    pdf = OUTPUT_DIR / (tex.stem + ".pdf")
    if not pdf.is_file():
        raise SystemExit(f"Expected output missing: {pdf}")
    print(f"[{name}] wrote {pdf.relative_to(ROOT)} ({pdf.stat().st_size // 1024} KiB)")
    return pdf


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--resume", action="store_true", help="Build the current resume (default)")
    group.add_argument("--template", action="store_true", help="Build the generic template")
    group.add_argument("--all", action="store_true", help="Build everything")
    args = parser.parse_args()

    if args.all:
        build_tex("resume")
        build_tex("template")
    elif args.template:
        build_tex("template")
    else:
        build_tex("resume")


if __name__ == "__main__":
    main()
