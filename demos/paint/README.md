# Paint

Status: Done (demo)

A small paint program. The canvas is its own surface, and the panel on the left is drawn on top of the window, so saving the canvas never includes the UI. Each stroke joins consecutive mouse samples with a line, so fast strokes have no gaps.

## Controls

| Input | Action |
|-------|--------|
| Left mouse (canvas) | Paint |
| Left mouse on a red / green / blue bar | Set that color channel (click or drag) |
| Mouse wheel | Brush size (shown in the panel) |
| S | Save the canvas as `painting_YYYYMMDD_HHMMSS.png` next to `main.py` (gitignored) |
| X | Clear the canvas |
| Esc | Quit |

## How to run

```sh
pip uninstall pygame          # pygame and pygame-ce both provide "import pygame" and conflict
pip install -r requirements.txt
python main.py
```

Needs Python 3.10+ (written for 3.13) and pygame-ce.
