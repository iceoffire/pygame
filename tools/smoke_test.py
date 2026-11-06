"""Launch every project headless for a few seconds and report crashes.

Usage (from the repo root, inside a venv with requirements.txt installed):
    python tools/smoke_test.py            # all projects
    python tools/smoke_test.py paint      # only projects whose path contains "paint"

Each project's Game loop reads SMOKE_FRAMES: it posts a few scripted key presses
(Enter, Space, arrows, P, R), then exits after that many frames.
The OpenGL demo needs a real display, so it's skipped.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"demos/opengl_3d"}
FRAMES = "900"
TIMEOUT = 120


def projects():
    for group in ("games", "demos"):
        for main in sorted((ROOT / group).glob("*/main.py")):
            yield main.parent


def main():
    only = sys.argv[1:]
    env = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy", SMOKE_FRAMES=FRAMES)
    failures = 0
    for project in projects():
        name = project.relative_to(ROOT).as_posix()
        if only and not any(o in name for o in only):
            continue
        if name in SKIP:
            print(f"SKIP  {name} (needs an OpenGL display)")
            continue
        result = None
        try:
            result = subprocess.run(
                [sys.executable, "main.py"], cwd=project, env=env,
                capture_output=True, text=True, timeout=TIMEOUT,
            )
            ok = result.returncode == 0
            detail = result.stderr.strip().splitlines()[-1:] if not ok else []
        except subprocess.TimeoutExpired:
            ok, detail = False, [f"did not exit within {TIMEOUT}s"]
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  -> {detail[0]}" if detail else ""))
        if not ok and result is not None and result.stderr:
            print("      " + result.stderr.strip().replace("\n", "\n      "))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
