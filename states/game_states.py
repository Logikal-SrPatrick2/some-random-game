from states.base_state import State
from states.manager import StateManager
from entities.player import Player
from entities.roaming_alien import RoamingAlien
from entities.entity_manager import EntityManager
from graphics.renderer import Renderer
from graphics.camera import Camera
from tiles.tile_manager import TileManager
from tiles.base_tile import DEFAULT_TILE_SIZE
from world.level_io import LevelIO
from entities.entity_factory import entity_factory
from systems.input_handler import InputHandler
from ui.pause_menu import PauseMenu
import pygame

class GameState(State):
    def __init__(self, manager: StateManager):
        super().__init__(manager)

    def player_input(self, inputs):
        pass
    
    def tick(self, dt):
        pass

    def render(self, graphics):
        pass

class WorldState(State):
    def __init__(self, manager, world_filename):
        super().__init__(manager)

        self.camera = Camera(1280, 720)

        self.tile_manager = TileManager()
        self.objects.append(self.tile_manager)

        self.entity_manager = EntityManager()
        self.objects.append(self.entity_manager)

        LevelIO.load_level(world_filename, self.tile_manager, self.entity_manager, entity_factory)

        self.camera.lock_to_entity(self.entity_manager.player)

        self.map_width = self.tile_manager.cols * DEFAULT_TILE_SIZE
        self.map_height = self.tile_manager.rows * DEFAULT_TILE_SIZE

    def player_input(self, inputs: InputHandler):
        super().player_input(inputs)

        if inputs.escape_tapped:
            print("WORLDSTATE: PAUSED")
            self.manager.push(PauseState(self.manager))
    
    def tick(self, dt):
        super().tick(dt)
        self.camera.tick(self.map_width, self.map_height)

    def render(self, graphics: Renderer):
        super().render(graphics)

class PauseState(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.blocks_ticking = True
        self.pause_menu = PauseMenu(manager=manager)
        self.objects.append(self.pause_menu)

class InventoryState(State):
    pass

class GameOverState(State):
    pass