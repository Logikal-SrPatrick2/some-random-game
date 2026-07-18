from enum import Enum, auto
from utils.vector2f import Vector2f
import math

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

    def check_sector_vs_box(self, sector_center: Vector2f, facing_angle_deg: int, r_tl: Vector2f) -> bool:
        """
        collision detection of r=256, theta=90deg sector to this hitbox
        """
        if self.type == HitboxType.RECTANGLE:
            radius = 256.0
            half_w = self.w_or_r / 2.0
            half_h = self.height / 2.0
            rect_center = r_tl + Vector2f(half_w, half_h)

            diff = sector_center - rect_center
            dist_x = abs(diff.x)
            dist_y = abs(diff.y)

            if dist_x > (half_w + radius) or dist_y > (half_h + radius): 
                return False

            circle_touches = False
            if dist_x <= half_w or dist_y <= half_h: 
                circle_touches = True
            elif (dist_x - half_w) ** 2 + (dist_y - half_h) ** 2 < radius ** 2:
                circle_touches = True

            if not circle_touches:
                return False

            if r_tl.x <= sector_center.x <= (r_tl.x + self.w_or_r) and \
            r_tl.y <= sector_center.y <= (r_tl.y + self.height):
                return True

            facing_rad = math.radians(facing_angle_deg)
            facing_dir = Vector2f(math.cos(facing_rad), -math.sin(facing_rad))

            corners = [
                r_tl,                                         # tl
                r_tl + Vector2f(self.w_or_r, 0),         # tr
                r_tl + Vector2f(0, self.height),         # bl
                r_tl + Vector2f(self.w_or_r, self.height) # br
            ]

            for corner in corners:
                to_corner = corner - sector_center
                dist_sq = to_corner.length_squared()
                
                if dist_sq <= radius ** 2:
                    dot = to_corner.x * facing_dir.x + to_corner.y * facing_dir.y
                    if dot > 0 and (dot ** 2) >= (dist_sq * 0.5):
                        return True

            rad_left = math.radians(facing_angle_deg + 45)
            rad_right = math.radians(facing_angle_deg - 45)
            
            ray_left_end = sector_center + Vector2f(math.cos(rad_left), -math.sin(rad_left)) * radius
            ray_right_end = sector_center + Vector2f(math.cos(rad_right), -math.sin(rad_right)) * radius

            if self.check_line_segment_vs_aabb(sector_center, ray_left_end, r_tl, self.w_or_r, self.height):
                return True
                
            if self.check_line_segment_vs_aabb(sector_center, ray_right_end, r_tl, self.w_or_r, self.height):
                return True

        return False

    def check_line_segment_vs_aabb(self, p1: Vector2f, p2: Vector2f, box_tl: Vector2f, box_w: float, box_h: float) -> bool:
        # application of liang-barsky
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        
        t0, t1 = 0.0, 1.0
        box_br = box_tl + Vector2f(box_w, box_h)
        for p, q in [(-dx, p1.x - box_tl.x), (dx, box_br.x - p1.x),
                    (-dy, p1.y - box_tl.y), (dy, box_br.y - p1.y)]:
            if p == 0:
                if q < 0:
                    return False
            else:
                t = q / p
                if p < 0:
                    if t > t1: return False
                    if t > t0: t0 = t
                else:
                    if t < t0: return False
                    if t < t1: t1 = t
                    
        return t0 <= t1