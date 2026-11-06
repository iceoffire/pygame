# Personal Projects using Pygame

This repo was originally used to save projects I built while studying Digital Games at FATEC Antônio Russo.

Pygame is a really fun library for making games, and I'm happy to contribute to the community by sharing my code here.

All projects target **Python 3.13** and **[pygame-ce](https://pyga.me)** (the community edition of pygame).

## Projects

### Games

| Project | Status | What it is |
|---------|--------|------------|
| [Space Invaders](games/space_invaders) | Playable | Vertical shooter with waves, an animated parallax background and a high score. |
| [Block Breaker](games/block_breaker) | Playable | Breakout clone with several levels and multi-hit bricks. You aim the ball by where it hits the paddle. |
| [Ninja Platformer](games/ninja_platformer) | Playable | Platformer whose levels are generated from a PNG image. |
| [Idle Gas Station](games/idle_gas_station) | WIP | Brazilian-themed idle clicker: click the flag, earn R$, buy upgrades. |

### Demos

| Project | What it shows |
|---------|---------------|
| [Ball Toward Mouse](demos/ball_toward_mouse) | Oblique throw physics with a trajectory preview, like Angry Birds. |
| [Particle System](demos/particle_system) | CPU particle fire following the mouse. |
| [Paint](demos/paint) | Simple paint program with a color picker, brush size and PNG export. |
| [Tilemap Surface](demos/tilemap_surface) | Builds a single tilemap surface from a PNG map (a simplified version of the Ninja Platformer maps). |
| [OpenGL 3D](demos/opengl_3d) | A textured 3D cube rendered with PyOpenGL inside a pygame window. |

Each project's README lists its controls.

## How to run

1. Install [Python 3.13](https://www.python.org/downloads/) or newer.
2. If you have the classic `pygame` package installed, remove it first. It conflicts with pygame-ce, because both provide the `pygame` module:

   ```
   pip uninstall pygame
   ```

3. Go to a project folder, install its requirements and run it:

   ```
   cd games/space_invaders
   pip install -r requirements.txt
   python main.py
   ```

   Use `python3` instead of `python` on Linux and some macOS setups.

## Repository layout

```
games/       playable games (title screen, pause, game over)
demos/       small tech experiments
_template/   starting point for new projects
tools/       smoke_test.py runs every project headless
```

Every project runs on its own from its folder. Games follow the same layout:

```
main.py          entry point
settings.py      screen size, FPS, speeds, colors
game/            app loop, scenes, entities, asset cache
assets/images/   images (snake_case names, zero-padded frames)
```

To start a new project, copy `_template/` and edit `settings.py`.

## Smoke test

Runs each project without a window for a few seconds, with scripted key presses, and reports crashes:

```
pip install -r requirements.txt
python tools/smoke_test.py
```

## Screenshots

**Ninja Platformer.** The map is drawn in `assets/images/maps/map_1.png`: ⬛ dirt, 🟦 spawn, 🟥 objective, ⬜ empty. Also on the [pygame forum](https://www.pygame.org/project/3530).

![Ninja Platformer](https://user-images.githubusercontent.com/36308052/206822181-a90bce15-e524-47d4-81be-0534f04ac48e.png)

**Particle System.** Also on the [pygame forum](https://www.pygame.org/project/3529).

![Particle System](https://user-images.githubusercontent.com/36308052/206822198-96ea1cd0-7f84-4f1d-81ab-a78f05c760f8.png)

**Space Invaders**

![Space Invaders](https://user-images.githubusercontent.com/36308052/206822288-e90ad759-f9c9-4525-b1e9-dc2b5da979d9.png)
