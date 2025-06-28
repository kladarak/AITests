import pygame
from pathlib import Path

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Point and Click Demo")

    # Set up asset paths using pathlib
    assets_dir = Path(__file__).parent / "assets"
    background_img = pygame.image.load(str(assets_dir / "astronomy_tower.jpeg"))
    # character_img = pygame.image.load(str(assets_dir / "character.png"))

    # character_pos = [100, 300]  # Example position

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background
        screen.blit(background_img, (0, 0))
        # screen.blit(character_img, character_pos)
        pygame.display.flip()

    pygame.quit()

