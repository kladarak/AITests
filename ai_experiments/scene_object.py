import pygame

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

    def update_image(self):
        self.image = pygame.image.load(str(self.img_path))
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self, surface):
        if not self.found:
            if self.animating:
                # Scale down for animation
                scale = max(0, 1 - self.animation_progress)
                w = max(1, int(self.rect.width * scale))
                h = max(1, int(self.rect.height * scale))
                img = pygame.transform.scale(self.image, (w, h))
                x = self.rect.x + (self.rect.width - w) // 2
                y = self.rect.y + (self.rect.height - h) // 2
                surface.blit(img, (x, y))
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