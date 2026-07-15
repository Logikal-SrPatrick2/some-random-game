from tiles.base_tile import Tile

class FloorPlain(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=0, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class FloorDown(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=1, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class FloorLeft(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=2, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class FloorDL(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=3, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class FloorUL(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=4, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class FloorRight(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=5, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class FloorDR(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=6, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class FloorUR(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=7, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class FloorUp(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=8, grid_x=grid_x, grid_y=grid_y, is_solid=False,
                         is_animated=False)
        
class WallBack(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=9, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallLeft(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=10, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallRight(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=11, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallRightCorner(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=12, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallLeftCorner(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=13, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF1_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=14, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF1_1(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=15, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF2_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=16, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF3_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=17, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF3_1(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=18, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF4_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=19, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF5_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=20, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF6_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=21, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF7_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=22, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF8_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=23, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallF9_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=24, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallP1_0(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=25, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallP1_1(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=26, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallPCrack1(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=27, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallPCrack2(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=28, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallPCrack3(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=29, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
        
class WallSolid(Tile):
    def __init__(self, grid_x: int, grid_y: int):
        super().__init__(tile_id=30, grid_x=grid_x, grid_y=grid_y, is_solid=True,
                         is_animated=False)
"""
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
"""
