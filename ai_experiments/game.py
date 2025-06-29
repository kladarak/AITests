import time
import random
import pygame
from .constants import CONSTANTS
from .scene_data_manager import SceneDataManager
from .scene import Scene
from .scene_editor import SceneEditor
from .ui import UICheckbox, UICounter, UITimer, UIWellDone

class WiggleTimer:
    def __init__(self):
        self.reset(time.time())

    def reset(self, now):
        self.last_found_time = now
        self.interval = random.randint(CONSTANTS.WIGGLE_MIN_SECONDS, CONSTANTS.WIGGLE_MAX_SECONDS)

    def should_wiggle(self, now):
        return (now - self.last_found_time) > self.interval

class Game:
    INVENTORY_HEIGHT = CONSTANTS.INVENTORY_HEIGHT

    def __init__(self):
        pygame.init()
        self.assets_dir = CONSTANTS.ASSETS_DIR
        self.data_file = CONSTANTS.DATA_FILE
        self.data_manager = SceneDataManager(self.data_file)
        self.scene = Scene(self.assets_dir, self.data_manager)
        self.editor = SceneEditor(self.scene)
        # Extend window height for inventory
        self.screen = pygame.display.set_mode(
            (self.scene.bg_width, self.scene.bg_height + self.INVENTORY_HEIGHT)
        )
        pygame.display.set_caption("Point and Click Demo")
        self.font = pygame.font.SysFont(None, CONSTANTS.FONT_SIZE)
        self.editor_mode = False
        self.game_won = False
        self.running = True
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.current_time = self.start_time
        self.elapsed_time = 0
        self.time_since_found = 0
        self.wiggle_timer = WiggleTimer()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            checkbox_rect = pygame.Rect(*CONSTANTS.CHECKBOX_POS, *CONSTANTS.CHECKBOX_SIZE)
            if event.type == pygame.MOUSEBUTTONDOWN and checkbox_rect.collidepoint(event.pos):
                self.editor_mode = not self.editor_mode
            elif self.editor_mode:
                self.editor.handle_event(event)
            elif not self.editor_mode and not self.game_won:
                # Game mode: check for item clicks
                key, obj = self.scene.get_object_at_pos(event.pos) if event.type == pygame.MOUSEBUTTONDOWN else (None, None)
                if obj:
                    obj.start_animation()
                    self.wiggle_timer.reset(self.current_time)
            # Handle restart button
            if self.game_won and event.type == pygame.MOUSEBUTTONDOWN:
                btn_rect = pygame.Rect(
                    self.scene.bg_width // 2 - CONSTANTS.RESTART_BTN_OFFSET_X,
                    self.scene.bg_height // 2 + CONSTANTS.RESTART_BTN_OFFSET_Y,
                    CONSTANTS.RESTART_BTN_WIDTH,
                    CONSTANTS.RESTART_BTN_HEIGHT
                )
                if btn_rect.collidepoint(event.pos):
                    self.scene.reset_all()
                    self.game_won = False
                    self.start_time = time.time()
                    self.wiggle_timer.reset(self.start_time)

    def update(self):
        self.current_time = time.time()
        self.elapsed_time = self.current_time - self.start_time
        self.time_since_found = self.current_time - self.wiggle_timer.last_found_time

        if self.editor_mode:
            self.editor.update()
        else:
            self.scene.update_animations()
            # Wiggle logic
            if not self.game_won:
                if self.wiggle_timer.should_wiggle(self.current_time):
                    unfound = [k for k, o in self.scene.objects.items() if not o.found]
                    if unfound:
                        wiggle_key = random.choice(unfound)
                        self.scene.objects[wiggle_key].start_wiggle(self.current_time)
                        self.wiggle_timer.reset(self.current_time)

    def render_inventory(self):
        # Draw black background for inventory
        inv_rect = pygame.Rect(0, self.scene.bg_height, self.scene.bg_width, self.INVENTORY_HEIGHT)
        pygame.draw.rect(self.screen, (0, 0, 0), inv_rect)

        # Draw found items as icons in a 2-row grid
        found_objs = [obj for obj in self.scene.objects.values() if obj.found]
        rows = CONSTANTS.INVENTORY_ROWS
        padding = CONSTANTS.INVENTORY_PADDING
        icon_height = (self.INVENTORY_HEIGHT - (rows + 1) * padding) // rows
        icon_width = icon_height  # Make icons square

        # Calculate how many columns fit
        cols = max(1, (self.scene.bg_width - padding) // (icon_width + padding))

        for idx, obj in enumerate(found_objs):
            row = idx // cols
            col = idx % cols
            if row >= rows:
                break  # Don't draw more than fits in the grid
            x = padding + col * (icon_width + padding)
            y = self.scene.bg_height + padding + row * (icon_height + padding)
            icon = pygame.transform.scale(obj.image, (icon_width, icon_height))
            self.screen.blit(icon, (x, y))

    def render(self):
        # Draw main scene
        self.scene.draw(self.screen, current_time=self.current_time)
        UICheckbox.draw(self.screen, self.editor_mode, self.font)

        # Game mode UI
        if not self.editor_mode:
            remaining = sum(1 for obj in self.scene.objects.values() if not obj.found)
            UICounter.draw(self.screen, remaining, self.font)
            UITimer.draw(self.screen, self.elapsed_time, self.font)
            if remaining == 0:
                self.game_won = True
                UIWellDone.draw(self.screen, self.font, self.scene)
        # Editor mode UI
        if self.editor_mode:
            self.editor.draw_status(self.screen, self.font)

        # Draw inventory section
        self.render_inventory()

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
        pygame.quit()

def run_game():
    Game().run()

if __name__ == "__main__":
    run_game()

