# Block Breaker

A Breakout-style game drawn entirely with pygame primitives. Bounce the ball off
your paddle to clear every brick across three levels. Where the ball hits the
paddle sets its angle, the ball speeds up on every paddle hit, and armored
bricks in level 3 take several hits (their color shows how many are left).
Your best score is saved to `save.json`.

## Controls

| Key | Action |
|-----|--------|
| A / D or Left / Right | Move the paddle |
| Mouse | Move the paddle |
| Space or left click | Launch the ball |
| P or Esc | Pause / resume |
| Q (paused) | Quit to title |
| Enter | Start (title screen) |
| R | Retry (game over / win) |
| Esc (game over / win) | Back to title |

## How to run

```bash
pip uninstall pygame          # pygame and pygame-ce both provide "pygame" and conflict
pip install -r requirements.txt
python main.py
```

Requires Python 3.10+ and pygame-ce 2.5+.

## Status

Playable.
