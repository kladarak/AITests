# ai_experiments/README.md

# Point and Click Hidden Object Game

## Overview

This is a point-and-click hidden object game built with Pygame. Players must find all hidden items in a scene by clicking on them. The game features an editor mode for adjusting item positions and sizes, an inventory display, a timer, and a hint system that wiggles an item if the player is stuck.

---

## Features

- **Game Mode:**  
  - Find all hidden items by clicking on them.
  - Items animate and disappear when found.
  - A counter shows how many items remain.
  - A timer displays elapsed time.
  - If the player is stuck (no item found for 20–30 seconds), a random unfound item wiggles as a hint.
  - When all items are found, a "Well done!" message and a Restart button appear.
  - Found items are shown in a 2-row inventory grid at the bottom of the screen.

- **Editor Mode:**  
  - Toggle editor mode using the checkbox in the top left.
  - Drag and resize items to adjust their positions and sizes.
  - Changes are saved to a scene data file.

---

## Controls

- **Left Click:**  
  - In game mode: Find items by clicking them.
  - In editor mode: Select and drag items.
  - Click the checkbox to toggle editor mode.
  - Click the Restart button to reset the game after winning.

- **Arrow Keys (Editor Mode):**  
  - Resize selected item (Up/Down).

---

## UI Elements

- **Checkbox (Top Left):** Toggle between game and editor mode.
- **Counter:** Shows how many items remain to be found.
- **Timer:** Shows elapsed time.
- **Inventory:** Found items are displayed as icons in a grid at the bottom.
- **Restart Button:** Appears after all items are found.

---

## Configuration

All configurable constants (paths, UI sizes, wiggle timing, etc.) are in `constants.py`:
- Inventory height, rows, padding
- Wiggle timer min/max seconds
- Restart button size and position
- Asset paths

---

## How to Run

1. Install [Pygame](https://www.pygame.org/):  
   `pip install pygame`
2. Place your assets (background, items, potions) in the appropriate folders as defined in `constants.py`.
3. Run the game:
   ```
   python -m ai_experiments.game
   ```

---

## File Structure

- `game.py` — Main game loop and logic
- `scene.py` — Scene and object management
- `scene_object.py` — SceneObject class (item logic and animation)
- `scene_editor.py` — Editor mode logic
- `scene_data_manager.py` — Load/save scene data
- `ui.py` — UI components (checkbox, counter, timer, well done)
- `constants.py` — All configurable constants

---

## Customization

- Add or remove items by placing/removing PNGs in the items/potions folders.
- Adjust UI and game behavior by editing `constants.py`.

---

## License

MIT License (or your chosen license)
