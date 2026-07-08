from tiles.base_tile import Tile

class Floor(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=0, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False, startIndex=0)

class Drainage(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=1, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False, startIndex=1)

class Barricade(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=2, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False, startIndex=2)
