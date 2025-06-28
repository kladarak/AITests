import pygame
import math

class SceneObject:
    def __init__(self, key, img_path, obj_data):
        self.key = key
        self.img_path = img_path
        self.image = pygame.image.load(str(img_path))
        self.rect = pygame.Rect(
            obj_data["x"], obj_data["y"], obj_data["width"], obj_data["height"]
        )
        self.update_image()
        self.found = False
        self.animating = False
        self.animation_progress = 0  # 0 to 1
        # Wiggle state
        self.wiggling = False
        self.wiggle_start_time = 0
        self.wiggle_duration = 1.0  # seconds

    def update_image(self):
        self.image = pygame.image.load(str(self.img_path))
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self, surface, current_time=None):
        if self.found:
            return
        if self.animating:
            # Scale down for animation
            scale = max(0, 1 - self.animation_progress)
            w = max(1, int(self.rect.width * scale))
            h = max(1, int(self.rect.height * scale))
            img = pygame.transform.scale(self.image, (w, h))
            x = self.rect.x + (self.rect.width - w) // 2
            y = self.rect.y + (self.rect.height - h) // 2
            surface.blit(img, (x, y))
        elif self.wiggling and current_time is not None:
            # Wiggle: oscillate horizontally
            elapsed = current_time - self.wiggle_start_time
            if elapsed < self.wiggle_duration:
                amplitude = 10
                freq = 8
                offset = int(amplitude * math.sin(freq * elapsed * 2 * math.pi))
                x = self.rect.x + offset
                surface.blit(self.image, (x, self.rect.y))
            else:
                self.wiggling = False
                surface.blit(self.image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)

    def start_animation(self):
        self.animating = True
        self.animation_progress = 0

    def update_animation(self, dt=0.05):
        if self.animating:
            self.animation_progress += dt
            if self.animation_progress >= 1:
                self.animating = False
                self.found = True

    def start_wiggle(self, current_time):
        self.wiggling = True
        self.wiggle_start_time = current_time