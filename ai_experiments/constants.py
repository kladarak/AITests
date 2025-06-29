from pathlib import Path

class CONSTANTS:
    ASSETS_DIR = Path(__file__).parent / "assets"
    DATA_FILE = ASSETS_DIR / "scene_data.json"
    BACKGROUND_IMAGE = ASSETS_DIR / "astronomy_tower.jpeg"
    ITEMS_DIR = ASSETS_DIR / "items"
    POTIONS_DIR = ASSETS_DIR / "potions"
    CHECKBOX_POS = (10, 10)
    CHECKBOX_SIZE = (24, 24)
    CHECKBOX_LABEL = "Editor Mode"
    OBJECT_DEFAULT = {"x": 0, "y": 0, "width": 100, "height": 100}
    FONT_SIZE = 24

    # Inventory
    INVENTORY_HEIGHT = 100
    INVENTORY_ROWS = 2
    INVENTORY_PADDING = 10

    # Wiggle
    WIGGLE_MIN_SECONDS = 20
    WIGGLE_MAX_SECONDS = 30

    # Restart button
    RESTART_BTN_WIDTH = 120
    RESTART_BTN_HEIGHT = 40
    RESTART_BTN_OFFSET_X = 60
    RESTART_BTN_OFFSET_Y = 10