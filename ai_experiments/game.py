import pygame
from pathlib import Path
import json

class SceneDataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.load()

    def load(self):
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                return json.load(f)
        return {}

    def get_object_data(self, key, default):
        return self.data.get(key, default)

    def update_object(self, key, rect):
        self.data[key] = {
            "x": rect.x,
            "y": rect.y,
            "width": rect.width,
            "height": rect.height
        }
        self.save()

    def save(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

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

class Scene:
    def __init__(self, assets_dir, data_manager):
        self.assets_dir = assets_dir
        self.data_manager = data_manager
        self.objects = self.load_objects()
        self.background = pygame.image.load(str(self.assets_dir / "astronomy_tower.jpeg"))
        self.bg_width, self.bg_height = self.background.get_size()

    def load_objects(self):
        image_paths = list((self.assets_dir / "items").glob("*.png")) + list((self.assets_dir / "potions").glob("*.png"))
        objects = {}
        for img_path in image_paths:
            key = img_path.stem
            obj_data = self.data_manager.get_object_data(key, {"x": 0, "y": 0, "width": 100, "height": 100})
            objects[key] = SceneObject(key, img_path, obj_data)
        return objects

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        for obj in self.objects.values():
            obj.draw(surface)

    def get_object_at_pos(self, pos):
        for key, obj in self.objects.items():
            if obj.rect.collidepoint(pos):
                return key, obj
        return None, None

    def update_object(self, key):
        obj = self.objects[key]
        obj.update_image()
        self.data_manager.update_object(key, obj.rect)

class SceneEditor:
    def __init__(self, scene):
        self.scene = scene
        self.dragging_key = None
        self.offset_x = 0
        self.offset_y = 0
        self.resized = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            key, obj = self.scene.get_object_at_pos(event.pos)
            if obj:
                self.dragging_key = key
                mouse_x, mouse_y = event.pos
                self.offset_x = obj.rect.x - mouse_x
                self.offset_y = obj.rect.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_key:
                self.scene.update_object(self.dragging_key)
            self.dragging_key = None
        elif event.type == pygame.MOUSEMOTION and self.dragging_key:
            mouse_x, mouse_y = event.pos
            obj = self.scene.objects[self.dragging_key]
            obj.rect.x = mouse_x + self.offset_x
            obj.rect.y = mouse_y + self.offset_y
        elif event.type == pygame.KEYDOWN and self.dragging_key:
            obj = self.scene.objects[self.dragging_key]
            if event.key == pygame.K_UP:
                obj.rect.width += 5
                obj.rect.height += 5
                self.resized = True
            elif event.key == pygame.K_DOWN and obj.rect.width > 10 and obj.rect.height > 10:
                obj.rect.width -= 5
                obj.rect.height -= 5
                self.resized = True

    def update(self):
        if self.resized and self.dragging_key:
            obj = self.scene.objects[self.dragging_key]
            obj.update_image()
            self.scene.update_object(self.dragging_key)
            self.resized = False

    def draw_status(self, surface, font):
        if self.dragging_key:
            obj = self.scene.objects[self.dragging_key]
            pos_text = f"{self.dragging_key}: ({obj.rect.x}, {obj.rect.y}) {obj.rect.width}x{obj.rect.height}"
            text_surf = font.render(pos_text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topright=(self.scene.bg_width - 10, 10))
            surface.blit(text_surf, text_rect)

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

