import pygame
from pathlib import Path
import json

def run_game():
    pygame.init()

    # Set up asset paths using pathlib
    assets_dir = Path(__file__).parent / "assets"
    data_file = assets_dir / "scene_data.json"

    # Find all PNG files in assets/items and assets/potions
    image_paths = list((assets_dir / "items").glob("*.png")) + list((assets_dir / "potions").glob("*.png"))

    # Load scene data from JSON
    if data_file.exists():
        with open(data_file, "r") as f:
            scene_data = json.load(f)
    else:
        scene_data = {}

    # Load background
    background_img = pygame.image.load(str(assets_dir / "astronomy_tower.jpeg"))
    bg_width, bg_height = background_img.get_size()
    screen = pygame.display.set_mode((bg_width, bg_height))
    pygame.display.set_caption("Point and Click Demo")

    # Load all images and their rects
    objects = {}
    for img_path in image_paths:
        key = img_path.stem  # filename without extension
        # Get data or default
        obj_data = scene_data.get(key, {"x": 0, "y": 0, "width": 100, "height": 100})
        img = pygame.image.load(str(img_path))
        img = pygame.transform.scale(img, (obj_data["width"], obj_data["height"]))
        rect = img.get_rect(topleft=(obj_data["x"], obj_data["y"]))
        objects[key] = {"img_path": img_path, "img": img, "rect": rect}

    font = pygame.font.SysFont(None, 24)

    dragging_key = None
    offset_x = 0
    offset_y = 0
    resized = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key, obj in objects.items():
                    if obj["rect"].collidepoint(event.pos):
                        dragging_key = key
                        mouse_x, mouse_y = event.pos
                        offset_x = obj["rect"].x - mouse_x
                        offset_y = obj["rect"].y - mouse_y
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_key:
                    # Save new position to JSON on drop
                    obj = objects[dragging_key]
                    scene_data[dragging_key] = {
                        "x": obj["rect"].x,
                        "y": obj["rect"].y,
                        "width": obj["rect"].width,
                        "height": obj["rect"].height
                    }
                    with open(data_file, "w") as f:
                        json.dump(scene_data, f, indent=4)
                dragging_key = None
            elif event.type == pygame.MOUSEMOTION and dragging_key:
                mouse_x, mouse_y = event.pos
                obj = objects[dragging_key]
                obj["rect"].x = mouse_x + offset_x
                obj["rect"].y = mouse_y + offset_y
            elif event.type == pygame.KEYDOWN and dragging_key:
                obj = objects[dragging_key]
                # Resize with up/down arrows for quick scene setup
                if event.key == pygame.K_UP:
                    obj["rect"].width += 5
                    obj["rect"].height += 5
                    resized = True
                elif event.key == pygame.K_DOWN and obj["rect"].width > 10 and obj["rect"].height > 10:
                    obj["rect"].width -= 5
                    obj["rect"].height -= 5
                    resized = True

        # If resized, update image and save to JSON
        if resized and dragging_key:
            obj = objects[dragging_key]
            obj["img"] = pygame.image.load(str(obj["img_path"]))
            obj["img"] = pygame.transform.scale(obj["img"], (obj["rect"].width, obj["rect"].height))
            scene_data[dragging_key] = {
                "x": obj["rect"].x,
                "y": obj["rect"].y,
                "width": obj["rect"].width,
                "height": obj["rect"].height
            }
            with open(data_file, "w") as f:
                json.dump(scene_data, f, indent=4)
            resized = False

        # Draw background
        screen.blit(background_img, (0, 0))
        # Draw all objects
        for key, obj in objects.items():
            screen.blit(obj["img"], obj["rect"].topleft)

        # Draw position and size of dragged object in top right corner
        if dragging_key:
            obj = objects[dragging_key]
            pos_text = f"{dragging_key}: ({obj['rect'].x}, {obj['rect'].y}) {obj['rect'].width}x{obj['rect'].height}"
            text_surf = font.render(pos_text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topright=(bg_width - 10, 10))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()

    pygame.quit()

