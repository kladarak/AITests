import pygame
from pathlib import Path
from .scene_data_manager import SceneDataManager
from .scene import Scene
from .scene_editor import SceneEditor

def run_game():
    pygame.init()
    assets_dir = Path(__file__).parent / "assets"
    data_file = assets_dir / "scene_data.json"
    data_manager = SceneDataManager(data_file)
    scene = Scene(assets_dir, data_manager)
    editor = SceneEditor(scene)
    screen = pygame.display.set_mode((scene.bg_width, scene.bg_height))
    pygame.display.set_caption("Point and Click Demo")
    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            editor.handle_event(event)

        editor.update()
        scene.draw(screen)
        editor.draw_status(screen, font)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_game()

