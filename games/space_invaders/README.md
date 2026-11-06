# Space Invaders

A vertical shoot 'em up: waves of enemy ships fly down over an animated parallax
starfield, and you hold the line at the bottom of the screen. Each enemy type takes
more hits and is worth more points. Your ship shows its damage as you lose lives.

- Three hand-designed opening waves, then a difficulty curve: more rows, faster
  ships and quicker enemy fire with every wave.
- Enemies that slip past the bottom edge, ram you, or shoot you cost a life. After a
  hit you blink for about a second and can't be hurt again.
- High score saved to `save.json` (gitignored).

## Controls

| Key | Action |
|-----|--------|
| A / D or Left / Right | Move |
| Space | Shoot (hold for auto-fire) |
| P or Esc | Pause / resume |
| Q (paused) | Quit to title |
| Enter | Start (title screen) |
| R | Retry (game over) |
| Esc (title / game over) | Quit / back to title |

## How to run

This project uses [pygame-ce](https://pyga.me/). It conflicts with classic pygame,
so remove that first:

```sh
pip uninstall pygame
pip install -r requirements.txt
python main.py
```

Requires Python 3.10+.

## Status

Playable.
