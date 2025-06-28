import pygame
from pathlib import Path
import json

def run_game():
    pygame.init()

    # Set up asset paths using pathlib
    assets_dir = Path(__file__).parent / "assets"
    data_file = assets_dir / "scene_data.json"

    # Load scene data from JSON
    if data_file.exists():
        with open(data_file, "r") as f:
            scene_data = json.load(f)
    else:
        # Default values if file doesn't exist
        scene_data = {
            "books": {
                "x": 300,
                "y": 350,
                "width": 100,
                "height": 100
            }
        }

    background_img = pygame.image.load(str(assets_dir / "astronomy_tower.jpeg"))
    bg_width, bg_height = background_img.get_size()

    screen = pygame.display.set_mode((bg_width, bg_height))
    pygame.display.set_caption("Point and Click Demo")

    books_img = pygame.image.load(str(assets_dir / "books.png"))
    books_img = pygame.transform.scale(
        books_img, (scene_data["books"]["width"], scene_data["books"]["height"])
    )
    books_rect = books_img.get_rect(
        topleft=(scene_data["books"]["x"], scene_data["books"]["y"])
    )

    font = pygame.font.SysFont(None, 24)

    dragging = False
    offset_x = 0
    offset_y = 0
    resized = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if books_rect.collidepoint(event.pos):
                    dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = books_rect.x - mouse_x
                    offset_y = books_rect.y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    # Save new position to JSON on drop
                    scene_data["books"]["x"] = books_rect.x
                    scene_data["books"]["y"] = books_rect.y
                    with open(data_file, "w") as f:
                        json.dump(scene_data, f, indent=4)
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = event.pos
                books_rect.x = mouse_x + offset_x
                books_rect.y = mouse_y + offset_y
            elif event.type == pygame.KEYDOWN:
                # Resize with up/down arrows for quick scene setup
                if event.key == pygame.K_UP:
                    books_rect.width += 5
                    books_rect.height += 5
                    resized = True
                elif event.key == pygame.K_DOWN and books_rect.width > 10 and books_rect.height > 10:
                    books_rect.width -= 5
                    books_rect.height -= 5
                    resized = True

        # If resized, update image and save to JSON
        if resized:
            books_img = pygame.image.load(str(assets_dir / "books.png"))
            books_img = pygame.transform.scale(books_img, (books_rect.width, books_rect.height))
            scene_data["books"]["width"] = books_rect.width
            scene_data["books"]["height"] = books_rect.height
            with open(data_file, "w") as f:
                json.dump(scene_data, f, indent=4)
            resized = False

        # Draw background
        screen.blit(background_img, (0, 0))
        # Draw books item
        screen.blit(books_img, books_rect.topleft)

        # Draw position in top right corner
        pos_text = f"({books_rect.x}, {books_rect.y}) {books_rect.width}x{books_rect.height}"
        text_surf = font.render(pos_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(topright=(bg_width - 10, 10))
        screen.blit(text_surf, text_rect)

        pygame.display.flip()

    pygame.quit()

