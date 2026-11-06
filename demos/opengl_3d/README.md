# OpenGL 3D

Status: Done (demo)

A textured cube drawn with legacy (fixed-function) OpenGL through PyOpenGL inside a pygame window. The texture is `assets/textures/dirt.jpg`, uploaded with `pygame.image.tobytes`. The window title also lists the controls, because drawing text in a raw OpenGL window takes extra work.

## Controls

Hold a key to keep moving.

| Input | Action |
|-------|--------|
| A / S / D | Rotate around the X / Y / Z axis |
| R / F | Zoom out / in |
| Arrow keys | Move the cube |
| Esc | Quit |

## How to run

```sh
pip uninstall pygame          # pygame and pygame-ce both provide "import pygame" and conflict
pip install -r requirements.txt
python main.py
```

Needs Python 3.10+ (written for 3.13) and pygame-ce and PyOpenGL (needs a real display with OpenGL; the headless smoke test skips this demo).
