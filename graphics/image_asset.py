import pygame
from graphics.render_mode import RenderMode

class ImageAsset:
    def __init__(self, file_path=None, surface=None):
        if file_path:
            self.surface = pygame.image.load(file_path).convert_alpha()
        else:
            self.surface = surface

    def resize(self, width: float, height: float):
        self.surface = pygame.transform.scale(self.surface, (int(width), int(height)))

    def tick(self, dt):
        pass

    def render(self, graphics, x, y, mode: RenderMode = RenderMode.TOP_LEFT):
        if mode == RenderMode.CENTER:
            render_x = x - (self.surface.get_width() / 2)
            render_y = y - (self.surface.get_height() / 2)
        else:
            render_x = x
            render_y = y

        graphics.draw_surface(self.surface, render_x, render_y)