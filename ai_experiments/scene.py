import pygame
from .scene_object import SceneObject
from .constants import CONSTANTS

class Scene:
    def __init__(self, assets_dir, data_manager):
        self.assets_dir = assets_dir
        self.data_manager = data_manager
        self.objects = self.load_objects()
        self.background = pygame.image.load(str(CONSTANTS.BACKGROUND_IMAGE))
        self.bg_width, self.bg_height = self.background.get_size()

    def load_objects(self):
        image_paths = list(CONSTANTS.ITEMS_DIR.glob("*.png")) + list(CONSTANTS.POTIONS_DIR.glob("*.png"))
        objects = {}
        for img_path in image_paths:
            key = img_path.stem
            obj_data = self.data_manager.get_object_data(key, CONSTANTS.OBJECT_DEFAULT)
            objects[key] = SceneObject(key, img_path, obj_data)
        return objects

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        for obj in self.objects.values():
            obj.draw(surface)

    def get_object_at_pos(self, pos):
        for key, obj in self.objects.items():
            if not obj.found and obj.rect.collidepoint(pos):
                return key, obj
        return None, None

    def update_object(self, key):
        obj = self.objects[key]
        obj.update_image()
        self.data_manager.update_object(key, obj.rect)

    def update_animations(self):
        for obj in self.objects.values():
            obj.update_animation()

    def reset_all(self):
        for obj in self.objects.values():
            obj.found = False
            obj.animating = False
            obj.animation_progress = 0