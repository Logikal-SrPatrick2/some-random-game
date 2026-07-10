from systems.input_handler import InputHandler
from graphics.renderer import Renderer
from entities.entity_manager import EntityManager
from entities.player import Player
from entities.roaming_alien import RoamingAlien
import pygame

WHITE = (255,255,255)
CRIMSON_SCARLET = (225, 45, 55)
CHARCOAL = (24, 20, 20)

class HUD:
    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager
        self.player = entity_manager.player
        self.elements = []
        self.elements.append(TargetHealthIndicator(self.player))

    def player_input(self, inputs: InputHandler):
        for element in self.elements:
            element.player_input(inputs)

    def tick(self, dt: float):
        for element in self.elements:
            element.tick(dt)

    def render(self, graphics: Renderer):
        for element in self.elements:
            element.render(graphics)

class TargetHealthIndicator:
    def __init__(self, player: Player):
        self.player = player
        self.target = None

    def player_input(self, inputs: InputHandler):
        pass

    def tick(self, dt: float):
        self.target = self.player.closest_creature

    def render(self, graphics: Renderer):

        if self.target:
            if isinstance(self.target, RoamingAlien):
                length = int(graphics.orbitron.size("Roaming Alien")[0])
                h = int(graphics.orbitron.size("Roaming Alien")[1])
                health = str(int(self.target.health))
                length2 = int(graphics.orbitron.size(health)[0])
                x = 1280//2 - length - 100
                graphics.draw_text("Roaming Alien", WHITE, x, 25, customFont=graphics.orbitron)
                x = 1280//2 + length + 100 - length2
                graphics.draw_text(health, WHITE, x, 25, customFont=graphics.orbitron)

                bar_length = 200 + 2*length
                percent = self.target.health / self.target.max_health
                x = 1280//2 - length - 100
                h = 30 + h

                if percent < 1:
                    graphics.draw_rect(x, h, bar_length, 10, CHARCOAL)

                graphics.draw_rect(x, h, int(bar_length*percent), 10, CRIMSON_SCARLET)