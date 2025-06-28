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
    books_rect = books_img.get_rect(topleft=(300, 350))

    font = pygame.font.SysFont(None, 24)

    dragging = False
    offset_x = 0
    offset_y = 0

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
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = event.pos
                books_rect.x = mouse_x + offset_x
                books_rect.y = mouse_y + offset_y

        # Draw background
        screen.blit(background_img, (0, 0))
        # Draw books item
        screen.blit(books_img, books_rect.topleft)

        # Draw position in top right corner
        pos_text = f"({books_rect.x}, {books_rect.y})"
        text_surf = font.render(pos_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(topright=(bg_width - 10, 10))
        screen.blit(text_surf, text_rect)

        pygame.display.flip()

    pygame.quit()

