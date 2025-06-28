import pygame

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