import pygame
from pathlib import Path

def run_game():
    pygame.init()

    # Set up asset paths using pathlib
    assets_dir = Path(__file__).parent / "assets"
    background_img = pygame.image.load(str(assets_dir / "astronomy_tower.jpeg"))
    bg_width, bg_height = background_img.get_size()

    screen = pygame.display.set_mode((bg_width, bg_height))
    pygame.display.set_caption("Point and Click Demo")

    books_img = pygame.image.load(str(assets_dir / "books.png"))
    books_img = pygame.transform.scale(books_img, (100, 100))
    books_pos = (300, 350)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background
        screen.blit(background_img, (0, 0))
        # Draw books item
        screen.blit(books_img, books_pos)
        pygame.display.flip()

    pygame.quit()

