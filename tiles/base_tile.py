from utils.vector2f import Vector2f

DEFAULT_TILE_SIZE = 128

class Tile:
    def __init__(self, tile_id: int, grid_x: int, grid_y: int, is_solid: bool = False,
                 is_animated: bool = False):
        self.id = tile_id
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.is_solid = is_solid
        self.is_animated = is_animated
        
        # TOP LEFT World Space Coordinates
        self.world_x = grid_x * DEFAULT_TILE_SIZE
        self.world_y = grid_y * DEFAULT_TILE_SIZE

        self.graphics_asset = None

    def on_collide(self, entity):
        pass

    def player_input(self, inputs):
        pass

    def tick(self, dt: float):
        if self.is_animated and self.graphics_asset:
            self.graphics_asset.tick(dt)

    def render(self, graphics, camera):
        if not self.graphics_asset:
            return

        world_pos = Vector2f(self.world_x, self.world_y)
        screen_pos = camera.to_screen_coords(world_pos)

        self.graphics_asset.render(graphics, screen_pos.x, screen_pos.y)