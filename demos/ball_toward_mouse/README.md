# Ball Toward Mouse

Status: Done (demo)

An oblique throw with gravity. Aim with the mouse: the yellow line runs from the ball to the cursor and a dotted line previews the path, using the same physics as the real throw. Click to throw. The ball bounces off the floor and the side walls, loses speed on every bounce, and resets on its own once it comes to rest.

Physics runs in fixed 1/120 s steps, measured in pixels and seconds, so the throw is the same at any frame rate. Tune gravity, launch strength, drag and bounciness in `settings.py`.

## Controls

| Input | Action |
|-------|--------|
| Mouse | Aim |
| Left click | Throw |
| R | Reset the ball |
| Esc | Quit |

## How to run

```sh
pip uninstall pygame          # pygame and pygame-ce both provide "import pygame" and conflict
pip install -r requirements.txt
python main.py
```

Needs Python 3.10+ (written for 3.13) and pygame-ce.
