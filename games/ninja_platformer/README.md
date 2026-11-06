# Ninja Platformer

A small platformer whose levels are built from images. Every pixel of a map
image becomes a 128x128 tile, and each floor tile picks its look (left end,
middle, right end; grass top, dirt below, floating) from its neighbours. Run and
jump the ninja to the objective on every map; after the last one you get your
completion time. The fastest run is saved to `save.json`.

The jump has coyote time (you can still jump just after running off a ledge),
jump buffering (a jump pressed just before landing still happens) and variable
height (let go early for a short hop). Fall off the map and you respawn at the
start of it.

## Making maps

Maps live in `assets/images/maps/map_<n>.png` and are played in order. Add a
`map_3.png` and it becomes the third map, no code change needed. Use this color
schema:

| Color | RGB | Description |
| ----- | --- | ----------- |
| ⬛ | (0, 0, 0) | dirt / floor |
| 🟦 | (0, 0, 255) | spawn |
| 🟥 | (255, 0, 0) | objective |
| ⬜ | anything else | nothing |

## Controls

| Key | Action |
|-----|--------|
| A / D or Left / Right | Run |
| Space / W / Up | Jump (hold for a higher jump) |
| P or Esc | Pause / resume |
| R | Restart the map (back to the spawn) |
| Q (paused) | Quit to title |
| Enter | Start (title screen) / play again (win screen) |
| Esc (title / win) | Quit / back to title |

## How to run

```bash
pip uninstall pygame          # pygame and pygame-ce both provide "pygame" and conflict
pip install -r requirements.txt
python main.py
```

Requires Python 3.10+ and pygame-ce 2.5+.

## Status

Playable.
