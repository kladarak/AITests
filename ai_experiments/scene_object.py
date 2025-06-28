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

    def update_image(self):
        self.image = pygame.image.load(str(self.img_path))
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)