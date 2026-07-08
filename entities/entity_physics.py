from utils.vector2f import Vector2f
from entities.hitbox import Hitbox, HitboxType
from tiles.base_tile import DEFAULT_TILE_SIZE


class EntityPhysics:
    def __init__(self, x: float, y: float, width: float, height: float,
                 vx: float = 0.0, vy: float = 0.0,
                 ax: float = 0.0, ay: float = 0.0):
        self.position = Vector2f(x, y)
        self.velocity = Vector2f(vx, vy)
        self.acceleration = Vector2f(ax, ay)
       
        self.width = width
        self.height = height


        self.hitboxes = []
        self.main_hitbox = None


    def add_hitbox(self, hitbox: Hitbox, is_main: bool = False):
        self.hitboxes.append(hitbox)
        if is_main:
            hitbox.is_solid = True
            self.main_hitbox = hitbox


    def remove_hitbox(self, hitbox: Hitbox):
        if hitbox in self.hitboxes:
            self.hitboxes.remove(hitbox)
        if self.main_hitbox == hitbox:
            self.main_hitbox = None


    def accelerate_tick(self, dt: float):
        self.velocity += self.acceleration * dt


    def movement_tick(self, dt: float, entity_manager=None, tile_manager=None, entity_parent=None):
        displacement = self.velocity * dt
        if displacement.is_zero:
            if tile_manager and self.main_hitbox:
                self._check_tile_collisions(self.position, tile_manager, entity_parent)
            return


        if not self.main_hitbox:
            self.position += displacement
            return


        max_step_x = self.main_hitbox.w_or_r if self.main_hitbox.type == HitboxType.RECTANGLE else self.main_hitbox.w_or_r * 2.0
        max_step_y = self.main_hitbox.height if self.main_hitbox.type == HitboxType.RECTANGLE else self.main_hitbox.w_or_r * 2.0


        steps_x = 1 if abs(displacement.x) <= max_step_x else int(abs(displacement.x) / max_step_x) + 1
        steps_y = 1 if abs(displacement.y) <= max_step_y else int(abs(displacement.y) / max_step_y) + 1


        step_dx = displacement.x / steps_x
        step_dy = displacement.y / steps_y


        for _ in range(steps_x):
            if step_dx == 0:
                break
            potential_pos = Vector2f(self.position.x + step_dx, self.position.y)
           
            tile_blocked = False
            if tile_manager:
                tile_blocked = self._check_tile_collisions(potential_pos, tile_manager, entity_parent)
               
            if tile_blocked:
                break


            collided_x, obstacle_phys = self._check_manager_collisions(potential_pos, entity_manager)
            if not collided_x:
                self.position.x = potential_pos.x
            else:
                self._snap_to_obstacle_x(step_dx, obstacle_phys)
                break


        for _ in range(steps_y):
            if step_dy == 0:
                break
            potential_pos = Vector2f(self.position.x, self.position.y + step_dy)
           
            tile_blocked = False
            if tile_manager:
                tile_blocked = self._check_tile_collisions(potential_pos, tile_manager, entity_parent)
               
            if tile_blocked:
                break


            collided_y, obstacle_phys = self._check_manager_collisions(potential_pos, entity_manager)
            if not collided_y:
                self.position.y = potential_pos.y
            else:
                self._snap_to_obstacle_y(step_dy, obstacle_phys)
                break


    def _check_manager_collisions(self, prospective_pos: Vector2f, entity_manager):
        if not entity_manager or not self.main_hitbox:
            return False, None

        candidates = entity_manager.spatial_grid.get_nearby_at(
            prospective_pos.x, prospective_pos.y, self.width, self.height
        )

        for other in candidates:
            other_phys = other.physics
            if other_phys is self:
                continue
            if not other_phys.main_hitbox:
                continue
            if self._will_collide(prospective_pos, other_phys):
                return True, other_phys

        return False, None


    def _check_tile_collisions(self, potential_pos: Vector2f, tile_manager, entity_parent) -> bool:
        my_box = self.main_hitbox
        my_tl = my_box.get_absolute_position(potential_pos, self.width, self.height)
       
        my_br_x = my_tl.x + (my_box.w_or_r if my_box.type == HitboxType.RECTANGLE else my_box.w_or_r * 2.0)
        my_br_y = my_tl.y + (my_box.height if my_box.type == HitboxType.RECTANGLE else my_box.w_or_r * 2.0)


        start_x = max(0, int(my_tl.x // DEFAULT_TILE_SIZE))
        end_x = min(tile_manager.cols - 1, int(my_br_x // DEFAULT_TILE_SIZE))
        start_y = max(0, int(my_tl.y // DEFAULT_TILE_SIZE))
        end_y = min(tile_manager.rows - 1, int(my_br_y // DEFAULT_TILE_SIZE))


        hit_solid = False


        for ty in range(start_y, end_y + 1):
            for tx in range(start_x, end_x + 1):
                tile = tile_manager.tilemap[ty][tx]
               
                tile_left = tile.world_x
                tile_right = tile.world_x + DEFAULT_TILE_SIZE
                tile_top = tile.world_y
                tile_bottom = tile.world_y + DEFAULT_TILE_SIZE


                if (my_tl.x < tile_right and my_br_x > tile_left and
                    my_tl.y < tile_bottom and my_br_y > tile_top):
                   
                    tile.on_collide(entity_parent)
                   
                    if tile.is_solid:
                        hit_solid = True


        return hit_solid


    def _will_collide(self, potential_pos: Vector2f, other_phys: 'EntityPhysics') -> bool:
        my_box = self.main_hitbox
        other_box = other_phys.main_hitbox


        my_tl = my_box.get_absolute_position(potential_pos, self.width, self.height)
        other_tl = other_box.get_absolute_position(other_phys.position, other_phys.width, other_phys.height)


        if my_box.type == HitboxType.RECTANGLE and other_box.type == HitboxType.RECTANGLE:
            return (my_tl.x < other_tl.x + other_box.w_or_r and
                    my_tl.x + my_box.w_or_r > other_tl.x and
                    my_tl.y < other_tl.y + other_box.height and
                    my_tl.y + my_box.height > other_tl.y)
           
        elif my_box.type == HitboxType.CIRCLE and other_box.type == HitboxType.CIRCLE:
            my_center = potential_pos + my_box.offset
            other_center = other_phys.position + other_box.offset
            distance_sq = (my_center.x - other_center.x)**2 + (my_center.y - other_center.y)**2
            radius_sum = my_box.w_or_r + other_box.w_or_r
            return distance_sq < radius_sum**2


        return False


    def _snap_to_obstacle_x(self, dx: float, other: 'EntityPhysics'):
        my_box = self.main_hitbox
        other_box = other.main_hitbox
        other_tl_x = other_box.get_absolute_position(other.position, other.width, other.height).x
       
        if dx > 0:  
            target_tl_x = other_tl_x - my_box.w_or_r
            self.position.x = target_tl_x - my_box.offset.x + (self.width / 2.0)
        elif dx < 0:  
            target_tl_x = other_tl_x + other_box.w_or_r
            self.position.x = target_tl_x - my_box.offset.x + (self.width / 2.0)


    def _snap_to_obstacle_y(self, dy: float, other: 'EntityPhysics'):
        my_box = self.main_hitbox
        other_box = other.main_hitbox
        other_tl_y = other_box.get_absolute_position(other.position, other.width, other.height).y
       
        if dy > 0:
            target_tl_y = other_tl_y - my_box.height
            self.position.y = target_tl_y - my_box.offset.y + (self.height / 2.0)
        elif dy < 0:  
            target_tl_y = other_tl_y + other_box.height
            self.position.y = target_tl_y - my_box.offset.y + (self.height / 2.0)