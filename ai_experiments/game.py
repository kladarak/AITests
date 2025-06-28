import pygame
from .constants import CONSTANTS
from .scene_data_manager import SceneDataManager
from .scene import Scene
from .scene_editor import SceneEditor

def draw_checkbox(surface, checked, font):
    box_rect = pygame.Rect(*CONSTANTS.CHECKBOX_POS, *CONSTANTS.CHECKBOX_SIZE)
    pygame.draw.rect(surface, (255, 255, 255), box_rect, 2)
    if checked:
        pygame.draw.line(surface, (0, 255, 0), (14, 22), (22, 14), 3)
        pygame.draw.line(surface, (0, 255, 0), (14, 14), (22, 22), 3)
    label = font.render(CONSTANTS.CHECKBOX_LABEL, True, (255, 255, 255))
    surface.blit(label, (CONSTANTS.CHECKBOX_POS[0] + CONSTANTS.CHECKBOX_SIZE[0] + 6, CONSTANTS.CHECKBOX_POS[1]))
    return box_rect

def run_game():
    pygame.init()
    assets_dir = CONSTANTS.ASSETS_DIR
    data_file = CONSTANTS.DATA_FILE
    data_manager = SceneDataManager(data_file)
    scene = Scene(assets_dir, data_manager)
    editor = SceneEditor(scene)
    screen = pygame.display.set_mode((scene.bg_width, scene.bg_height))
    pygame.display.set_caption("Point and Click Demo")
    font = pygame.font.SysFont(None, CONSTANTS.FONT_SIZE)

    editor_mode = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            checkbox_rect = pygame.Rect(*CONSTANTS.CHECKBOX_POS, *CONSTANTS.CHECKBOX_SIZE)
            if event.type == pygame.MOUSEBUTTONDOWN and checkbox_rect.collidepoint(event.pos):
                editor_mode = not editor_mode
            elif editor_mode:
                editor.handle_event(event)

        if editor_mode:
            editor.update()
        scene.draw(screen)
        draw_checkbox(screen, editor_mode, font)
        if editor_mode:
            editor.draw_status(screen, font)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_game()

