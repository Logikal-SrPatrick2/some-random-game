import pygame

class Button:
    def __init__(self, x, y, width, height, text, on_click=None, on_hover=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        
        self.on_click_callback = on_click
        self.on_hover_callback = on_hover
        
        self.is_hovered = False
        self.is_pressed = False
        
        self.color = (50, 50, 70)
        self.text_color = (255, 255, 255)

    def player_input(self, inputs):
        self.is_hovered = self.rect.collidepoint(inputs.mouse_pos)
    
        if self.is_hovered and inputs.mouse_clicked[0]:
            self._on_click()

    def tick(self, dt):
        if self.is_hovered:
            self._on_hover()
        else:
            self.color = (50, 50, 70) 

    def render(self, graphics):
        graphics.draw_rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.color)
        
        text_x = self.rect.x + (self.rect.width // 2)
        text_y = self.rect.y + (self.rect.height // 2)
        graphics.draw_text_centered(self.text, self.text_color, text_x, text_y)

    def _on_click(self):
        if self.on_click_callback:
            self.on_click_callback()

    def _on_hover(self):
        if self.on_hover_callback:
            self.on_hover_callback() 
        else:
            self.color = (70, 70, 100)