from utils.vector2f import Vector2f
from tiles.tile_types import FloorPlain, FloorDown, FloorLeft, FloorDL, FloorUL, FloorRight, FloorDR, FloorUR, FloorUp
from tiles.tile_types import WallBack, WallLeft, WallRight, WallRightCorner, WallLeftCorner
from tiles.tile_types import WallF1_0, WallF1_1, WallF2_0, WallF3_0, WallF3_1, WallF4_0, WallF5_0, WallF6_0, WallF7_0, WallF8_0, WallF9_0
from tiles.tile_types import WallP1_0, WallP1_1, WallPCrack1, WallPCrack2, WallPCrack3, WallSolid
from graphics.animation import Animation
from graphics.spritesheet import Spritesheet
from utils.conversion_to_exe import resource_path
from tiles.base_tile import DEFAULT_TILE_SIZE
from tiles import TILE_IMAGE_ASSETS

TILE_FACTORY = {
    0: FloorPlain,
    1: FloorDown,
    2: FloorLeft,
    3: FloorDL,
    4: FloorUL,
    5: FloorRight,
    6: FloorDR,
    7: FloorUR,
    8: FloorUp,
    9: WallBack,
    10: WallLeft,
    11: WallRight,
    12: WallRightCorner,
    13: WallLeftCorner,
    14: WallF1_0,
    15: WallF1_1,
    16: WallF2_0,
    17: WallF3_0,
    18: WallF3_1,
    19: WallF4_0,
    20: WallF5_0,
    21: WallF6_0,
    22: WallF7_0,
    23: WallF8_0,
    24: WallF9_0,
    25: WallP1_0,
    26: WallP1_1,
    27: WallPCrack1,
    28: WallPCrack2,
    29: WallPCrack3,
    30: WallSolid
}

class TileManager:
    def __init__(self):
        """
        img_path = resource_path("res/spritesheets/tilemap/tilemap.png")
        json_path = resource_path("res/spritesheets/tilemap/tilemap.json")

        self.master_spritesheet = Spritesheet(img_path, json_path).get_frames()
        
        for sprite in self.master_spritesheet:
            sprite.resize(DEFAULT_TILE_SIZE, DEFAULT_TILE_SIZE)
        """

        self.tilemap = [] 
        self.cols = 0
        self.rows = 0
        self.sprites = {}  

    def load_map(self, map_data: list[list[int]]):
        self.rows = len(map_data)
        self.cols = len(map_data[0]) if self.rows > 0 else 0
        self.tilemap = []

        for y in range(self.rows):
            row = []
            for x in range(self.cols):
                tile_id = map_data[y][x]
                tile_class = TILE_FACTORY.get(tile_id, FloorPlain)
                tile = tile_class(grid_x=x, grid_y=y)

                if tile.is_animated:
                    pass
                    #tile.graphics_asset = Animation(self.master_spritesheet[tile.startIndex:tile.stopIndex+1])
                else:
                    tile.graphics_asset = TILE_IMAGE_ASSETS[tile.id]

                row.append(tile)
                
            self.tilemap.append(row)

    def player_input(self, inputs):
        if self.tilemap:
            for y in range(self.rows):
                for x in range(self.cols):
                    self.tilemap[y][x].player_input(inputs)

    def tick(self, dt: float):
        if self.tilemap:
            for y in range(self.rows):
                for x in range(self.cols):
                    self.tilemap[y][x].tick(dt)
    
    def audio(self, mixer):
        pass

    def render(self, graphics, camera):
        if self.tilemap:
            start_col = max(0, int(camera.position.x // DEFAULT_TILE_SIZE))
            end_col = min(self.cols, int((camera.position.x + camera.screen_width) // DEFAULT_TILE_SIZE) + 1)
            
            start_row = max(0, int(camera.position.y // DEFAULT_TILE_SIZE))
            end_row = min(self.rows, int((camera.position.y + camera.screen_height) // DEFAULT_TILE_SIZE) + 1)

            for y in range(start_row, end_row):
                for x in range(start_col, end_col):
                    tile = self.tilemap[y][x]
                    tile.render(graphics, camera)