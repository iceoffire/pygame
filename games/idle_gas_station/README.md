# Idle Gas Station

**Status: WIP**

A small Brazilian-themed idle clicker. Click the Brazilian flag to toss a banknote and earn
Reais (R$), then spend them on upgrades that earn money for you every second, even while
the game is closed.

- Click the flag: a bill falls and you earn its value (floating `+R$ N`, flag squash).
- **Bigger Bills** raises the click value 1 → 2 → 5 → 10 → 20 → 50 → 100, and the falling
  bill shows the matching note.
- Idle upgrades: Underwear Size, Fuel Pump, Convenience Store, Car Wash, Oil Refinery.
  Prices grow exponentially (`base × growth^level`).
- Progress is saved to `save.json` (gitignored) every 10 seconds and on quit. When you come
  back you get the idle income for the time you were away, up to 8 hours.

The banknote images keep their original Portuguese print (and the flag is Brazil's): that's
the theme art. Everything the game itself draws is in English.

## Controls

| Input | Action |
|-------|--------|
| Left click on the flag / Space | Earn money |
| Left click on a card / 1–6 | Buy that upgrade |
| Mouse wheel / Up / Down | Scroll the upgrade list |
| P / Esc | Pause (Q in the pause menu returns to the title) |
| Enter or click | Start from the title screen |

## How to run

Needs Python 3.10+ and [pygame-ce](https://pyga.me/). pygame-ce and classic pygame both
provide the `pygame` module and conflict, so remove classic pygame first:

```sh
pip uninstall pygame
pip install -r requirements.txt
python main.py
```

Delete `save.json` to start over.

## Layout

```
main.py            entry point
settings.py        window size, colors, layout, timings
game/app.py        main loop, clock, scene stack
game/economy.py    upgrades, pricing, idle and offline income (no pygame)
game/format.py     R$ number formatting (no pygame)
game/ui.py         upgrade cards, drawn icons, image helpers
game/scenes/       title and play (+ pause) scenes
```
