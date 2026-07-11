import pygame

class InputHandler:
    def __init__(self):
        self.keys = []
        self.mouse_pos = (0, 0)
        self.mouse_buttons = (False, False, False)
        self.prev_mouse_buttons = (False, False, False)
        self.mouse_clicked = [False, False, False] 

        self.escape_tapped = False
        self.prev_escape = False
        self.escape = False

        self.t_tapped = False
        self.prev_t = False
        self.t = False

    def update_snapshot(self):
        self.prev_escape = self.escape
        self.prev_t = self.t

        self.keys = pygame.key.get_pressed()

        self.escape = self.keys[pygame.K_ESCAPE]
        self.escape_tapped = self.escape and not self.prev_escape

        self.t = self.keys[pygame.K_t]
        self.t_tapped = self.t and not self.prev_t

        self.mouse_pos = pygame.mouse.get_pos()
        
        self.prev_mouse_buttons = self.mouse_buttons
        self.mouse_buttons = pygame.mouse.get_pressed()
        
        self.mouse_clicked = [
            self.mouse_buttons[0] and not self.prev_mouse_buttons[0], 
            self.mouse_buttons[1] and not self.prev_mouse_buttons[1], 
            self.mouse_buttons[2] and not self.prev_mouse_buttons[2]
        ]