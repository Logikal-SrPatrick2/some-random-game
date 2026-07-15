from enum import Enum, auto
from utils.vector2f import Vector2f

SHOW_HITBOX = False

class HitboxType(Enum):
    RECTANGLE = auto()
    CIRCLE = auto()

class Hitbox:
    def __init__(self, name: str, hitbox_type: HitboxType, 
                 offset_x: float, offset_y: float, 
                 width_or_radius: float, height: float = 0.0, 
                 is_solid: bool = False,
                 on_collide_callback = None):
        self.name = name 
        self.type = hitbox_type
        self.offset = Vector2f(offset_x, offset_y)
        self.w_or_r = width_or_radius
        self.height = height
        self.is_solid = is_solid
        self.show_hitbox = SHOW_HITBOX

        self.on_collide_callback = on_collide_callback

    def get_absolute_position(self, entity_pos: Vector2f, entity_width: float, entity_height: float) -> Vector2f:
        top_left_x = entity_pos.x - (entity_width / 2.0)
        top_left_y = entity_pos.y - (entity_height / 2.0)
        return Vector2f(top_left_x + self.offset.x, top_left_y + self.offset.y)

    def on_collide(self, other_hitbox: 'Hitbox', owner_entity, other_entity):
        if self.on_collide_callback:
            self.on_collide_callback(other_hitbox, owner_entity, other_entity)