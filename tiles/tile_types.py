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
        
class WallR(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=3, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False, startIndex=3)
        
class WallL(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=4, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False, startIndex=4)
        
class WallFull(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=5, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False, startIndex=5)
        
class WallD(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=6, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False, startIndex=6)
        
class WallDL(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=7, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False, startIndex=7)
        
class WallDR(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=8, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False, startIndex=8)
