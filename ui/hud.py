from systems.input_handler import InputHandler
from graphics.renderer import Renderer
from entities.utils.entity_manager import EntityManager
from entities.creatures.player import Player
from entities.creatures.roaming_alien import RoamingAlien
from pygame import Surface, SRCALPHA

WHITE = (255,255,255)
CRIMSON_SCARLET = (225, 45, 55)
MINT_GREEN = (50, 205, 125)
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

        self.health_surf = Surface((96, 32), SRCALPHA).convert_alpha()
        self.health_surf.fill((50, 205, 125, 127))

        self.enemy_health_surf = Surface((96, 32), SRCALPHA).convert_alpha()
        self.enemy_health_surf.fill((225, 45, 55, 127))

    def player_input(self, inputs: InputHandler):
        pass

    def tick(self, dt: float):
        self.target = self.player.closest_creature

    def render(self, graphics: Renderer):

        name = "Player"
        if self.player:
            health = str(int(self.player.health))
            lenh = int(graphics.orbitron.size(health)[0])
            heighth = int(graphics.orbitron.size(health)[1])
            barlen = 1280//5

            x = 32
            graphics.draw_text(name, WHITE, x, 25, customFont=graphics.orbitron)
            x += barlen
            graphics.draw_surface(self.health_surf, x-96, 25)
            x -= lenh
            graphics.draw_text(health, WHITE, x, 25, customFont=graphics.orbitron)

            percent = self.player.health / self.player.max_health
            x = 32
            heighth += 30

            if percent < 1:
                graphics.draw_rect(x, heighth, barlen, 10, CHARCOAL)

            graphics.draw_rect(x, heighth, int(barlen*percent), 10, MINT_GREEN)

        if self.target:
            if isinstance(self.target, RoamingAlien):
                length = int(graphics.orbitron.size("Roaming Alien")[0])
                h = int(graphics.orbitron.size("Roaming Alien")[1])
                health = str(int(self.target.health))
                length2 = int(graphics.orbitron.size(health)[0])

                bar_length = 1280//4

                x = 1280//2 - bar_length//2
                graphics.draw_text("Roaming Alien", WHITE, x, 25, customFont=graphics.orbitron)
                x += bar_length
                graphics.draw_surface(self.enemy_health_surf, x-96, 25)
                x -= length2
                graphics.draw_text(health, WHITE, x, 25, customFont=graphics.orbitron)

                
                percent = self.target.health / self.target.max_health
                x = 1280//2 - bar_length//2
                h = 30 + h

                if percent < 1:
                    graphics.draw_rect(x, h, bar_length, 10, CHARCOAL)

                graphics.draw_rect(x, h, int(bar_length*percent), 10, CRIMSON_SCARLET)