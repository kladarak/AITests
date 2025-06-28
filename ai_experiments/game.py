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

def draw_counter(surface, remaining, font):
    text = f"Items remaining: {remaining}"
    text_surf = font.render(text, True, (255, 255, 0))
    surface.blit(text_surf, (CONSTANTS.CHECKBOX_POS[0], CONSTANTS.CHECKBOX_POS[1] + 40))

def draw_well_done(surface, font, scene):
    msg = "Well done!"
    msg_surf = font.render(msg, True, (0, 255, 0))
    msg_rect = msg_surf.get_rect(center=(scene.bg_width // 2, scene.bg_height // 2 - 30))
    surface.blit(msg_surf, msg_rect)
    # Draw Restart button
    btn_rect = pygame.Rect(scene.bg_width // 2 - 60, scene.bg_height // 2 + 10, 120, 40)
    pygame.draw.rect(surface, (50, 50, 200), btn_rect)
    btn_text = font.render("Restart", True, (255, 255, 255))
    btn_text_rect = btn_text.get_rect(center=btn_rect.center)
    surface.blit(btn_text, btn_text_rect)
    return btn_rect

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
    game_won = False

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            checkbox_rect = pygame.Rect(*CONSTANTS.CHECKBOX_POS, *CONSTANTS.CHECKBOX_SIZE)
            if event.type == pygame.MOUSEBUTTONDOWN and checkbox_rect.collidepoint(event.pos):
                editor_mode = not editor_mode
            elif editor_mode:
                editor.handle_event(event)
            elif not editor_mode and not game_won:
                # Game mode: check for item clicks
                key, obj = scene.get_object_at_pos(event.pos) if event.type == pygame.MOUSEBUTTONDOWN else (None, None)
                if obj:
                    obj.start_animation()

            # Handle restart button
            if game_won and event.type == pygame.MOUSEBUTTONDOWN:
                btn_rect = pygame.Rect(scene.bg_width // 2 - 60, scene.bg_height // 2 + 10, 120, 40)
                if btn_rect.collidepoint(event.pos):
                    scene.reset_all()
                    game_won = False

        if editor_mode:
            editor.update()
        else:
            scene.update_animations()

        scene.draw(screen)
        draw_checkbox(screen, editor_mode, font)

        # Game mode UI
        if not editor_mode:
            remaining = sum(1 for obj in scene.objects.values() if not obj.found)
            draw_counter(screen, remaining, font)
            if remaining == 0:
                game_won = True
                btn_rect = draw_well_done(screen, font, scene)
        # Editor mode UI
        if editor_mode:
            editor.draw_status(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_game()

