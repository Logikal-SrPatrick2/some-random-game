import pygame

class Renderer:
    def __init__(self):
        self.window_surface = None
        self.default_font = None

    def initialize_display(self, width: int, height: int, caption: str):
        print(f"[RENDERER] Initializing window surface ({width}x{height})...")
        self.window_surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.default_font = pygame.font.Font(None, 14)
        self.large_font = pygame.font.Font(None, 56)
        self.orbitron = pygame.font.Font("res/fonts/Orbitron.ttf", 25)

    def clear(self, color=(0, 0, 0)):
        if self.window_surface:
            self.window_surface.fill(color)

    def draw_text(self, text: str, color: tuple, x: int, y: int, larger_font: bool = False, customFont: pygame.font.Font = None):
        if not customFont:
            if self.window_surface and self.default_font:
                if larger_font:
                    text_surface = self.large_font.render(text, True, color)
                else:
                    text_surface = self.default_font.render(text, True, color)
        else:
            if self.window_surface:
                text_surface = customFont.render(text, True, color)
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