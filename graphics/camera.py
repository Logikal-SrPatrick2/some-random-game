from utils.vector2f import Vector2f

class Camera:
    def __init__(self, screen_width: int, screen_height: int):
        self.position = Vector2f(0.0, 0.0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.target = None

    def lock_to_entity(self, entity):
        self.target = entity

    def tick(self, map_width_pixels: float = None, map_height_pixels: float = None):
        if not self.target:
            return

        self.position.x = self.target.physics.position.x - (self.screen_width / 2.0)
        self.position.y = self.target.physics.position.y - (self.screen_height / 2.0)

        if map_width_pixels is not None:
            max_cam_x = map_width_pixels - self.screen_width
            self.position.x = max(0.0, min(self.position.x, max_cam_x))

        if map_height_pixels is not None:
            max_cam_y = map_height_pixels - self.screen_height
            self.position.y = max(0.0, min(self.position.y, max_cam_y))

    def to_screen_coords(self, world_pos: Vector2f) -> Vector2f:
        return Vector2f(world_pos.x - self.position.x, world_pos.y - self.position.y)