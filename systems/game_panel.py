import pygame
import time
from systems.activation import initialize_system, terminate_system
from systems.input_handler import InputHandler
from graphics.renderer import Renderer
from auditory.mixer import Mixer
from auditory.audio_asset import AudioAsset

class GamePanel:
    def __init__(self, width, height, caption):
        initialize_system()

        AudioAsset.load_all_assets()

        self.input_handler = InputHandler()

        self.clock = pygame.time.Clock()
        self.accumulator = 0.0
        self.time_step = 1.0 / 60.0
        
        self.renderer = Renderer()
        self.renderer.initialize_display(width, height, caption)

        self.mixer = Mixer()

        from states.manager import StateManager
        from states.menu_states import MenuState, MainMenuState
        
        self.state_manager = StateManager()
        self.state_manager.change_state(MenuState(self.state_manager))
        self.state_manager.push(MainMenuState(self.state_manager))
        
        self.running = False

        self.last_input_ms = []
        self.last_tick_ms = []
        self.last_audio_ms = []
        self.last_render_ms = []

        self.iter_count = 60

    def start(self):
        print("[PANEL] GamePanel activated with Graphics Pipeline.")
        self.running = True
        self._loop()

    def _loop(self):
        while self.running:
            raw_dt = self.clock.tick() / 1000.0  
            if raw_dt > 0.1: # cap at 100ms
                raw_dt = 0.1
            self.accumulator += raw_dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # PLAYER INPUT START
            input_start = time.perf_counter()
            self.input_handler.update_snapshot()
            self.state_manager.player_input(self.input_handler)
            input_ms = (time.perf_counter() - input_start) * 1000.0
            if len(self.last_input_ms) >= self.iter_count:
                self.last_input_ms.pop(0)
            self.last_input_ms.append(input_ms)
            # PLAYER INPUT END

            # TICK START (pass time_step as dt)
            tick_start = time.perf_counter()
            while self.accumulator >= self.time_step:
                self.state_manager.tick(self.time_step)
                self.accumulator -= self.time_step
            tick_ms = (time.perf_counter() - tick_start) * 1000.0
            if len(self.last_tick_ms) >= self.iter_count:
                self.last_tick_ms.pop(0)
            self.last_tick_ms.append(tick_ms)
            # TICK END

            # AUDIO START
            audio_start = time.perf_counter()
            self.state_manager.audio(self.mixer)
            self.mixer.update()
            audio_ms = (time.perf_counter() - audio_start) * 1000.0
            if len(self.last_audio_ms) >= self.iter_count:
                self.last_audio_ms.pop(0)
            self.last_audio_ms.append(audio_ms)
            # AUDIO END
            
            # RENDER START
            render_start = time.perf_counter()
            self.renderer.clear((20, 20, 30))
            self.state_manager.render(self.renderer)
            render_ms = (time.perf_counter() - render_start) * 1000.0

            if len(self.last_render_ms) >= self.iter_count:
                self.last_render_ms.pop(0)
            self.last_render_ms.append(render_ms)

            #self._render_metrics(input_ms, tick_ms, audio_ms, render_ms)

            pygame.display.flip()
            # RENDER END
            
        print("[PANEL] Exiting loop.")
        pygame.display.quit()
        terminate_system()

    def _render_metrics(self, input_ms, tick_ms, audio_ms, render_ms):
        metrics_panel_width = 1280
        metrics_panel_height = 144

        self.renderer.draw_rect(0, 600, metrics_panel_width, metrics_panel_height, (0, 0, 0))
        self.renderer.draw_text(f"INPUT: {input_ms:.2f} ms", (255, 255, 255), 5, 605)
        self.renderer.draw_text(f"TICK: {tick_ms:.2f} ms", (255, 255, 255), 5, 625)
        self.renderer.draw_text(f"AUDIO: {audio_ms:.2f} ms", (255, 255, 255), 5, 645)
        self.renderer.draw_text(f"RENDER: {render_ms:.2f} ms", (255, 255, 255), 5, 665)

        self.renderer.draw_text(f"{self.iter_count}-IT-INPUT: {(sum(self.last_input_ms)/self.iter_count):.2f} ms", 
                                (255, 255, 255), 105, 605)
        self.renderer.draw_text(f"{self.iter_count}-IT-TICK: {(sum(self.last_tick_ms)/self.iter_count):.2f} ms", 
                                (255, 255, 255), 105, 625)
        self.renderer.draw_text(f"{self.iter_count}-IT-AUDIO: {(sum(self.last_audio_ms)/self.iter_count):.2f} ms", 
                                (255, 255, 255), 105, 645)
        self.renderer.draw_text(f"{self.iter_count}-IT-RENDER: {(sum(self.last_render_ms)/self.iter_count):.2f} ms", 
                                (255, 255, 255), 105, 665)
        
        top_state = self.state_manager.stack[-1]

        if hasattr(top_state, "entity_manager"):
            entity_manager_last_tick_ms = top_state.entity_manager.last_tick_ms

            self.renderer.draw_text(f"60-IT-ENTITIES-TICK: {(sum(entity_manager_last_tick_ms)/60):.2f} ms", 
                                (255, 255, 255), 205, 625)

        