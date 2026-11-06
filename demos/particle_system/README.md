# Particle System

Status: Done (demo)

A torch follows the (hidden) mouse cursor and emits fire particles. Particles and the glow use additive blending (`BLEND_ADD`), so overlapping flames brighten each other. `fire.png` is loaded once. Each particle draws a cached copy that is already scaled and dimmed, so nothing is reloaded or edited pixel by pixel while the demo runs. The spawn rate is in particles per second and doesn't depend on the frame rate.

## Controls

| Input | Action |
|-------|--------|
| Mouse | Move the torch |
| Mouse wheel | Change intensity (particles per second) |
| Esc | Quit |

## How to run

```sh
pip uninstall pygame          # pygame and pygame-ce both provide "import pygame" and conflict
pip install -r requirements.txt
python main.py
```

Needs Python 3.10+ (written for 3.13) and pygame-ce.
