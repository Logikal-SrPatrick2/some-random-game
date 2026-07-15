import pygame
from ui.button import Button

class PalettePanel:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.buttons = []
        self.active_sub_buttons = None
        self.active_brush_type = "TILE" # "TILE", "ENTITY", or "DELETE_ENTITY"
        self.active_id = 0 
        
        self.setup_palette()

    def floor_palette(self):
        sub_buttons = []

        sub_buttons.append(
            Button(
                self.rect.x, 60, 100, 40, "Plain",
                on_click=lambda: self.set_brush("TILE", 0)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+100, 60, 100, 40, "Down",
                on_click=lambda: self.set_brush("TILE", 1)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+200, 60, 100, 40, "Left",
                on_click=lambda: self.set_brush("TILE", 2)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+300, 60, 100, 40, "DL",
                on_click=lambda: self.set_brush("TILE", 3)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x, 100, 100, 40, "UL",
                on_click=lambda: self.set_brush("TILE", 4)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+100, 100, 100, 40, "Right",
                on_click=lambda: self.set_brush("TILE", 5)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+200, 100, 100, 40, "DR",
                on_click=lambda: self.set_brush("TILE", 6)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+300, 100, 100, 40, "UR",
                on_click=lambda: self.set_brush("TILE", 7)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x, 140, 100, 40, "Up",
                on_click=lambda: self.set_brush("TILE", 8)
            )
        )

        self.active_sub_buttons = sub_buttons

    def wall_palette(self):
        sub_buttons = []

        sub_buttons.append(
            Button(
                self.rect.x, 60, 100, 40, "Back",
                on_click=lambda: self.set_brush("TILE", 9)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+100, 60, 100, 40, "Left",
                on_click=lambda: self.set_brush("TILE", 10)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+200, 60, 100, 40, "Right",
                on_click=lambda: self.set_brush("TILE", 11)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+300, 60, 100, 40, "RCorner",
                on_click=lambda: self.set_brush("TILE", 12)
            )
        )

        sub_buttons.append(
            Button(
                self.rect.x, 100, 100, 40, "LCorner",
                on_click=lambda: self.set_brush("TILE", 13)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+100, 100, 100, 40, "F1.0",
                on_click=lambda: self.set_brush("TILE", 14)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+200, 100, 100, 40, "F1.1",
                on_click=lambda: self.set_brush("TILE", 15)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+300, 100, 100, 40, "F2.0",
                on_click=lambda: self.set_brush("TILE", 16)
            )
        )

        sub_buttons.append(
            Button(
                self.rect.x, 140, 100, 40, "F3.0",
                on_click=lambda: self.set_brush("TILE", 17)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+100, 140, 100, 40, "F3.1",
                on_click=lambda: self.set_brush("TILE", 18)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+200, 140, 100, 40, "F4.0",
                on_click=lambda: self.set_brush("TILE", 19)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+300, 140, 100, 40, "F5.0",
                on_click=lambda: self.set_brush("TILE", 20)
            )
        )

        sub_buttons.append(
            Button(
                self.rect.x, 180, 100, 40, "F6.0",
                on_click=lambda: self.set_brush("TILE", 21)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+100, 180, 100, 40, "F7.0",
                on_click=lambda: self.set_brush("TILE", 22)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+200, 180, 100, 40, "F8.0",
                on_click=lambda: self.set_brush("TILE", 23)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+300, 180, 100, 40, "F9.0",
                on_click=lambda: self.set_brush("TILE", 24)
            )
        )

        sub_buttons.append(
            Button(
                self.rect.x, 220, 100, 40, "Plain 1.0",
                on_click=lambda: self.set_brush("TILE", 25)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+100, 220, 100, 40, "Plain 1.1",
                on_click=lambda: self.set_brush("TILE", 26)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+200, 220, 100, 40, "PCrack 1",
                on_click=lambda: self.set_brush("TILE", 27)
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+300, 220, 100, 40, "PCrack 2",
                on_click=lambda: self.set_brush("TILE", 28)
            )
        )

        sub_buttons.append(
            Button(
                self.rect.x, 260, 100, 40, "PCrack 3",
                on_click=lambda: self.set_brush("TILE", 29)
            )
        )

        sub_buttons.append(
            Button(
                self.rect.x+100, 260, 100, 40, "Filled",
                on_click=lambda: self.set_brush("TILE", 30)
            )
        )

        self.active_sub_buttons = sub_buttons

    def entity_palette(self):
        sub_buttons = []
        sub_buttons.append(
            Button(
                self.rect.x, 60, 100, 40, "Player",
                on_click=lambda: self.set_brush("ENTITY", "Player")
            )
        )
        sub_buttons.append(
            Button(
                self.rect.x+100, 60, 100, 40, "Roaming Alien",
                on_click=lambda: self.set_brush("ENTITY", "RoamingAlien")
            )
        )

        sub_buttons.append(
            Button(
                self.rect.x, 500, 100, 40, "Delete",
                on_click=lambda: self.set_brush("DELETE_ENTITY", "Eraser")
            )
        )

        self.active_sub_buttons = sub_buttons

    def setup_palette(self):
        self.buttons.append(
            Button(
                self.rect.x,
                0,
                100,
                40,
                "Floor Tiles",
                on_click=lambda: self.floor_palette()
            )
        )
        self.buttons.append(
            Button(
                self.rect.x+100,
                0,
                100,
                40,
                "Wall Tiles",
                on_click=lambda: self.wall_palette()
            )
        )
        self.buttons.append(
            Button(
                self.rect.x+200,
                0,
                100,
                40,
                "Entities",
                on_click=lambda: self.entity_palette()
            )
        )
        """
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
        """

    def set_brush(self, brush_type, assignment):
        self.active_brush_type = brush_type
        self.active_id = assignment

    def player_input(self, inputs):
        for btn in self.buttons:
            btn.player_input(inputs)

        if self.active_sub_buttons:
            for btn in self.active_sub_buttons:
                btn.player_input(inputs)

    def tick(self, dt):
        for btn in self.buttons:
            btn.tick(dt)

        if self.active_sub_buttons:
            for btn in self.active_sub_buttons:
                btn.tick(dt)

    def render(self, graphics):
  
        graphics.draw_rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height, (30, 30, 40))
        for btn in self.buttons:
            btn.render(graphics)

        if self.active_sub_buttons:
            for btn in self.active_sub_buttons:
                btn.render(graphics)
            
      
        status_txt = f"Tool: {self.active_brush_type} ({self.active_id})"
        graphics.draw_text_centered(status_txt, (255, 255, 0), self.rect.x + (self.rect.width // 2), self.rect.y + self.rect.height - 30)