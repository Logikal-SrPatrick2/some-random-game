from utils.vector2f import Vector2f
from tiles.tile_types import Floor, Drainage, Barricade
from graphics.animation import Animation
from graphics.spritesheet import Spritesheet
from tiles.base_tile import DEFAULT_TILE_SIZE

TILE_FACTORY = {
    0: Floor,
    1: Drainage,
    2: Barricade
}

class TileManager:
    def __init__(self):
        img_path = "res/spritesheets/tilemap/tilemap.png"
        json_path = "res/spritesheets/tilemap/tilemap.json"

        self.master_spritesheet = Spritesheet(img_path, json_path).get_frames()
        
        for sprite in self.master_spritesheet:
            sprite.resize(DEFAULT_TILE_SIZE, DEFAULT_TILE_SIZE)

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
                tile_class = TILE_FACTORY.get(tile_id, Floor)
                tile = tile_class(grid_x=x, grid_y=y)

                if tile.is_animated:
                    tile.graphics_asset = Animation(self.master_spritesheet[tile.startIndex:tile.stopIndex+1])
                else:
                    tile.graphics_asset = self.master_spritesheet[tile.startIndex]

                row.append(tile)
                
            self.tilemap.append(row)

    def player_input(self, inputs):
        for y in range(self.rows):
            for x in range(self.cols):
                self.tilemap[y][x].player_input(inputs)

    def tick(self, dt: float):
        for y in range(self.rows):
            for x in range(self.cols):
                self.tilemap[y][x].tick(dt)

    def render(self, graphics, camera):
        start_col = max(0, int(camera.position.x // DEFAULT_TILE_SIZE))
        end_col = min(self.cols, int((camera.position.x + camera.screen_width) // DEFAULT_TILE_SIZE) + 1)
        
        start_row = max(0, int(camera.position.y // DEFAULT_TILE_SIZE))
        end_row = min(self.rows, int((camera.position.y + camera.screen_height) // DEFAULT_TILE_SIZE) + 1)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                tile = self.tilemap[y][x]
                tile.render(graphics, camera)