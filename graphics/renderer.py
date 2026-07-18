import pygame
import math
from utils.conversion_to_exe import resource_path

class Renderer:
    orbitron = None

    sector_surfs = []
    sector_surf_radius = 256

    def __init__(self):
        self.window_surface = None
        self.default_font = None

    def initialize_display(self, width: int, height: int, caption: str):
        print(f"[RENDERER] Initializing window surface ({width}x{height})...")
        self.window_surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.default_font = pygame.font.Font(None, 14)
        self.large_font = pygame.font.Font(None, 56)
        self.orbitron = pygame.font.Font(resource_path("res/fonts/Orbitron.ttf"), 25)
        Renderer.orbitron = self.orbitron

        self.init_sector_surfs()

    def init_sector_surfs(self):
        fill = (255, 0, 0, 100)
        outline = (255, 0, 0, 255)

        step = 2
        OUTLINE_WIDTH = 2
        sector_angle = 90
        half = sector_angle//2

        for angle in range(0, 360):
            d = Renderer.sector_surf_radius*2
            # Create the temporary full-sized surface
            temp_surf = pygame.Surface((d, d), pygame.SRCALPHA).convert_alpha()

            r = Renderer.sector_surf_radius
            local_center = (r, r)
            points = [local_center]

            start_angle = angle - half
            end_angle = angle + half

            start_normalized = start_angle % 360
            end_normalized = end_angle % 360

            actual_end = end_normalized
            if actual_end <= start_normalized:
                actual_end += 360

            for deg in range(int(start_normalized), int(actual_end) + 1, step):
                rad = math.radians(deg)
                px = r + r * math.cos(rad)
                py = r - r * math.sin(rad)
                points.append((px, py))

            if len(points) > 2:
                pygame.draw.polygon(temp_surf, fill, points)
                pygame.draw.polygon(temp_surf, outline, points, OUTLINE_WIDTH)

            rect = temp_surf.get_bounding_rect()
            
            cropped_surf = temp_surf.subsurface(rect)
            
            final_surf = cropped_surf.copy()

            offset_x = rect.x - r
            offset_y = rect.y - r

            Renderer.sector_surfs.append((final_surf, offset_x, offset_y))

    def clear(self, color=(0, 0, 0)):
        if self.window_surface:
            self.window_surface.fill(color)

    def draw_sector_standard(self, x: int, y: int, angle_facing: int):
        angle_facing = angle_facing % 360
        if self.window_surface:
            surf, offset_x, offset_y = Renderer.sector_surfs[angle_facing]
            
            top_left_x = x + offset_x
            top_left_y = y + offset_y
            
            self.window_surface.blit(surf, (top_left_x, top_left_y))

    def draw_text(self, text: str, color: tuple, x: int, y: int, larger_font: bool = False, customFont: pygame.font.Font = None, debug: bool = False):
        if not customFont:
            if self.window_surface and self.default_font:
                if larger_font:
                    text_surface = self.large_font.render(text, True, color)
                else:
                    text_surface = self.default_font.render(text, True, color)
        else:
            if self.window_surface:
                text_surface = customFont.render(text, True, color)

        if debug:
            print(x, y)
        self.window_surface.blit(text_surface, (x, y))

    def draw_text_centered(self, text: str, color: tuple, x: int, y: int, larger_font: bool = False, customFont: pygame.font.Font = None):
        if not customFont:
            if self.window_surface and self.default_font:
                if larger_font:
                    text_surface = self.large_font.render(text, True, color)
                else:
                    text_surface = self.default_font.render(text, True, color)
        else:
            if self.window_surface:
                text_surface = customFont.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.window_surface.blit(text_surface, text_rect)
            
    def draw_rect(self, x: int, y: int, width: int, height: int, color: tuple, alpha: int = 255):
        if not self.window_surface:
            return
        
        if alpha >= 255:
            pygame.draw.rect(self.window_surface, color, (x, y, width, height))
        elif alpha > 0:
            temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            pygame.draw.rect(temp_surface, (*color[:3], alpha), (0, 0, width, height))
            
            self.window_surface.blit(temp_surface, (x, y))

    def draw_rect_hollow(self, x: float, y: float, width: float, height: float, color: tuple, thickness: int = 2):
        if self.window_surface:
            rect = pygame.Rect(int(x), int(y), int(width), int(height))
            pygame.draw.rect(self.window_surface, color, rect, thickness)

    def draw_circle_hollow(self, center_x: float, center_y: float, radius: float, color: tuple, thickness: int = 2):
        if self.window_surface:
            pygame.draw.circle(self.window_surface, color, (int(center_x), int(center_y)), int(radius), thickness)

    def draw_surface(self, surface: pygame.Surface, x: float, y: float):
        if self.window_surface and surface:
            self.window_surface.blit(surface, (int(x), int(y)))