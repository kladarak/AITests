import pygame
from .constants import CONSTANTS

class UICheckbox:
    @staticmethod
    def draw(surface, checked, font):
        box_rect = pygame.Rect(*CONSTANTS.CHECKBOX_POS, *CONSTANTS.CHECKBOX_SIZE)
        pygame.draw.rect(surface, (255, 255, 255), box_rect, 2)
        if checked:
            pygame.draw.line(surface, (0, 255, 0), (14, 22), (22, 14), 3)
            pygame.draw.line(surface, (0, 255, 0), (14, 14), (22, 22), 3)
        label = font.render(CONSTANTS.CHECKBOX_LABEL, True, (255, 255, 255))
        surface.blit(label, (CONSTANTS.CHECKBOX_POS[0] + CONSTANTS.CHECKBOX_SIZE[0] + 6, CONSTANTS.CHECKBOX_POS[1]))
        return box_rect

class UICounter:
    @staticmethod
    def draw(surface, remaining, font):
        text = f"Items remaining: {remaining}"
        text_surf = font.render(text, True, (255, 255, 0))
        surface.blit(text_surf, (CONSTANTS.CHECKBOX_POS[0], CONSTANTS.CHECKBOX_POS[1] + 40))

class UITimer:
    @staticmethod
    def draw(surface, seconds, font):
        text = f"Time: {int(seconds)}s"
        text_surf = font.render(text, True, (255, 255, 255))
        surface.blit(text_surf, (CONSTANTS.CHECKBOX_POS[0], CONSTANTS.CHECKBOX_POS[1] + 70))

class UIWellDone:
    @staticmethod
    def draw(surface, font, scene):
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