# Tilemap Surface

Status: Done (demo)

A proof of concept for building a level from an image. Each pixel of a tiny map image (`assets/images/maps/map_N.png`, 10 x 10) becomes a 128 x 128 tile on one large surface. Black pixels become floor tiles (`assets/images/tiles/floor_mf.png`). The level is built once per map, then scaled to the window and blitted each frame.

## Controls

| Input | Action |
|-------|--------|
| 1 / 2 | Show map 1 / map 2 |
| Esc | Quit |

## How to run

```sh
pip uninstall pygame          # pygame and pygame-ce both provide "import pygame" and conflict
pip install -r requirements.txt
python main.py
```

Needs Python 3.10+ (written for 3.13) and pygame-ce.
