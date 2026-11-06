# Project template

Copy this folder to start a new project that already follows the repo's pattern.

```
cp -r _template games/my_game
```

## What you get

| File | Purpose |
|------|---------|
| `main.py` | Entry point: `Game(TitleScene).run()` |
| `settings.py` | Title, screen size, FPS, colors, speeds (units per second) |
| `game/app.py` | Loop with one persistent `Clock`, `dt` in seconds, one `event.get()` per frame, and a scene stack (`push`, `pop`, `switch`) |
| `game/scene.py` | `Scene` base class (`handle_event`, `update(dt)`, `draw`), plus `draw_text` and `dim` helpers |
| `game/assets.py` | Load-once cache: `image`, `frames`, `font`, `tinted` |
| `game/fx.py` | `ScreenShake`, `FloatingText` |
| `game/save.py` | High score saved to `save.json` (gitignored) |
| `game/scenes/` | Title, play and pause examples |

## Rules

- `snake_case` for files and assets, `PascalCase` for classes, constants in `settings.py`.
- Move things by `speed * dt`, never by a fixed amount per frame.
- Load images through `assets`, never inside `update` or `draw`.
- Keep the `SMOKE_FRAMES` hook in `app.py` so `tools/smoke_test.py` can run the project.
