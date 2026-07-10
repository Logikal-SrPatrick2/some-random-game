import pygame
from ui.button import Button

class PalettePanel:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.buttons = []
        self.active_brush_type = "TILE" # "TILE", "ENTITY", or "DELETE_ENTITY"
        self.active_id = 0 
        
        self.setup_palette()

    def setup_palette(self):
        # Tile Brushes
        self.buttons.append(Button(self.rect.x + 10, self.rect.y + 20, 180, 40, "Floor Tile", 
                                   on_click=lambda: self.set_brush("TILE", 0)))
        self.buttons.append(Button(self.rect.x + 10, self.rect.y + 70, 180, 40, "Drainage Tile", 
                                   on_click=lambda: self.set_brush("TILE", 1)))
        self.buttons.append(Button(self.rect.x + 10, self.rect.y + 120, 180, 40, "Barricade Tile", 
                                   on_click=lambda: self.set_brush("TILE", 2)))
        
        # Entity Brushes
        self.buttons.append(Button(self.rect.x + 10, self.rect.y + 180, 180, 40, "Spawn Player", 
                                   on_click=lambda: self.set_brush("ENTITY", "Player")))
        self.buttons.append(Button(self.rect.x + 10, self.rect.y + 230, 180, 40, "Spawn Alien", 
                                   on_click=lambda: self.set_brush("ENTITY", "RoamingAlien")))
        
        # more tile brushes
        self.buttons.append(Button(self.rect.x + 10, self.rect.y + 280, 40, 40, "R", 
                                   on_click=lambda: self.set_brush("TILE", 3)))
        self.buttons.append(Button(self.rect.x + 60, self.rect.y + 280, 40, 40, "L", 
                                   on_click=lambda: self.set_brush("TILE", 4)))
        self.buttons.append(Button(self.rect.x + 110, self.rect.y + 280, 40, 40, "Full", 
                                   on_click=lambda: self.set_brush("TILE", 5)))
        self.buttons.append(Button(self.rect.x + 10, self.rect.y + 350, 40, 40, "D", 
                                   on_click=lambda: self.set_brush("TILE", 6)))
        self.buttons.append(Button(self.rect.x + 60, self.rect.y + 350, 40, 40, "DL", 
                                   on_click=lambda: self.set_brush("TILE", 7)))
        self.buttons.append(Button(self.rect.x + 110, self.rect.y + 350, 40, 40, "DR", 
                                   on_click=lambda: self.set_brush("TILE", 8)))
        
        # Utility Brushes
        self.buttons.append(Button(self.rect.x + 10, self.rect.y + 400, 180, 40, "Delete Entity", 
                                   on_click=lambda: self.set_brush("DELETE_ENTITY", "Eraser")))

    def set_brush(self, brush_type, assignment):
        self.active_brush_type = brush_type
        self.active_id = assignment

    def player_input(self, inputs):
        for btn in self.buttons:
            btn.player_input(inputs)

    def tick(self, dt):
        for btn in self.buttons:
            btn.tick(dt)

    def render(self, graphics):
  
        graphics.draw_rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height, (30, 30, 40))
        for btn in self.buttons:
            btn.render(graphics)
            
      
        status_txt = f"Tool: {self.active_brush_type} ({self.active_id})"
        graphics.draw_text_centered(status_txt, (255, 255, 0), self.rect.x + (self.rect.width // 2), self.rect.y + self.rect.height - 30)