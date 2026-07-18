import pygame
from graphics.render_mode import RenderMode

class ImageAsset:
    def __init__(self, file_path=None, surface=None):
        if file_path:
            self.surface = pygame.image.load(file_path).convert_alpha()
        else:
            self.surface = surface

    def resize(self, width: float, height: float):
        target_w = int(width)
        target_h = int(height)
    
        if self.surface.get_width() == target_w and self.surface.get_height() == target_h:
            return
           
        self.surface = pygame.transform.scale(self.surface, (target_w, target_h))

    def rotate_and_copy(self, angle: int) -> 'ImageAsset':
        new_surface = pygame.transform.rotate(self.surface, angle)
        
        return ImageAsset(surface=new_surface)

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

    @property
    def calculate_auto_pivot(self) -> int:
        mask = pygame.mask.from_surface(self.surface)
        
        filled_pixels = mask.outline()
        
        if not filled_pixels:
            return self.surface.get_height() 
            
        lowest_y = max(p[1] for p in filled_pixels)
        
        return lowest_y