import time
import random
import pygame
from .constants import CONSTANTS
from .scene_data_manager import SceneDataManager
from .scene import Scene
from .scene_editor import SceneEditor
from .ui import UICheckbox, UICounter, UITimer, UIWellDone

def reset_wiggle_interval():
    """Helper to reset wiggle interval."""
    return random.randint(20, 30)

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

    start_time = time.time()
    last_found_time = start_time
    wiggle_interval = reset_wiggle_interval()

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time
        time_since_found = current_time - last_found_time

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
                    last_found_time = current_time
                    wiggle_interval = reset_wiggle_interval()
            # Handle restart button
            if game_won and event.type == pygame.MOUSEBUTTONDOWN:
                btn_rect = pygame.Rect(scene.bg_width // 2 - 60, scene.bg_height // 2 + 10, 120, 40)
                if btn_rect.collidepoint(event.pos):
                    scene.reset_all()
                    game_won = False
                    start_time = time.time()
                    last_found_time = start_time
                    wiggle_interval = reset_wiggle_interval()

        if editor_mode:
            editor.update()
        else:
            scene.update_animations()

            # Wiggle logic
            if not game_won:
                if time_since_found > wiggle_interval:
                    # Pick a random unfound item to wiggle
                    unfound = [k for k, o in scene.objects.items() if not o.found]
                    if unfound:
                        wiggle_key = random.choice(unfound)
                        scene.objects[wiggle_key].start_wiggle(current_time)
                        wiggle_interval = reset_wiggle_interval()
                        last_found_time = current_time  # Reset timer after wiggle
                # No need to handle wiggle drawing here; handled in SceneObject.draw

        scene.draw(screen, current_time=current_time)
        UICheckbox.draw(screen, editor_mode, font)

        # Game mode UI
        if not editor_mode:
            remaining = sum(1 for obj in scene.objects.values() if not obj.found)
            UICounter.draw(screen, remaining, font)
            UITimer.draw(screen, elapsed_time, font)
            if remaining == 0:
                game_won = True
                btn_rect = UIWellDone.draw(screen, font, scene)
        # Editor mode UI
        if editor_mode:
            editor.draw_status(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_game()

