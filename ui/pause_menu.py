from ui.button import Button
from systems.input_handler import InputHandler
from graphics.renderer import Renderer
from states.manager import StateManager
import pygame

class PauseMenu:
    def __init__(self, x: int = 320, y: int = 180, width: int = 640, height: int = 360, manager: StateManager = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state_manager = manager

        self.buttons = []

        self.resume_btn = Button(590, 300, 100, 50, 
                            "RESUME", 
                            on_click=self.resume_game,
                            on_hover=lambda: setattr(self.resume_btn, "color", (150, 50, 50))
                                )
        self.exit_btn = Button(590, 370, 100, 50, 
                            "LEAVE WORLD", 
                            on_click=self.exit_world,
                            on_hover=lambda: setattr(self.exit_btn, "color", (150, 50, 50))
                                )
        
        self.buttons.append(self.resume_btn)
        self.buttons.append(self.exit_btn)

    def player_input(self, inputs: InputHandler):
        for button in self.buttons:
            button.player_input(inputs)

        if inputs.escape_tapped:
            self.resume_game()

    def tick(self, dt: float):
        for button in self.buttons:
            button.tick(dt)

    def render(self, graphics: Renderer):
        graphics.draw_rect(self.x, self.y, self.width, self.height, (20, 20, 20))
        for button in self.buttons:
            button.render(graphics)

    def resume_game(self):
        self.state_manager.pop()

    def exit_world(self):
        from states.menu_states import MenuState, MainMenuState
        self.state_manager.change_state(MenuState(self.state_manager))
        self.state_manager.push(MainMenuState(self.state_manager))
