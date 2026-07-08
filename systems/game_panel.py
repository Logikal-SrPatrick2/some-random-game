import pygame
from systems.activation import initialize_system, terminate_system
from systems.input_handler import InputHandler
from graphics.renderer import Renderer

class GamePanel:
    def __init__(self, width, height, caption):
        initialize_system()

        self.input_handler = InputHandler()

        self.clock = pygame.time.Clock()
        self.accumulator = 0.0
        self.time_step = 1.0 / 60.0
        
        self.renderer = Renderer()
        self.renderer.initialize_display(width, height, caption)

        from states.manager import StateManager
        from states.menu_states import MenuState, MainMenuState
        
        self.state_manager = StateManager()
        self.state_manager.change_state(MenuState(self.state_manager))
        self.state_manager.push(MainMenuState(self.state_manager))
        
        self.running = False

    def start(self):
        print("[PANEL] GamePanel activated with Graphics Pipeline.")
        self.running = True
        self._loop()

    def _loop(self):
        while self.running:
            raw_dt = self.clock.tick() / 1000.0  
            self.accumulator += raw_dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # PLAYER INPUT START
            self.input_handler.update_snapshot()
            self.state_manager.player_input(self.input_handler)
            # PLAYER INPUT END

            # TICK START (pass time_step as dt)
            while self.accumulator >= self.time_step:
                self.state_manager.tick(self.time_step)
                self.accumulator -= self.time_step
            # TICK END
            
            # RENDER START
            self.renderer.clear((20, 20, 30))
            self.state_manager.render(self.renderer)
            pygame.display.flip()
            # RENDER END
            
        print("[PANEL] Exiting loop.")
        pygame.display.quit()
        terminate_system()