from entities.mechanics.hitbox import Hitbox, HitboxType
from entities.mechanics.spatial_grid import SpatialGrid
from entities.mechanics.entity_physics import EntityPhysics
from graphics.renderer import Renderer
from graphics.camera import Camera
from utils.vector2f import Vector2f
import time

class EntityManager:
    def __init__(self):
        self.entities = []
        self.solid_entities = []
        self.player = None
        self.spatial_grid = SpatialGrid()

        self.last_tick_ms = []

    def player_input(self, inputs):
        for entity in self.entities:
            entity.player_input(inputs)

    def tick(self, dt: float):
        start = time.perf_counter()

        self._rebuild_spatial_grid()
        # NAKAKALAG TO
        #self.check_triggers_tick()

        for entity in self.entities:
            entity.tick(dt)

        tick_ms = (time.perf_counter() - start) * 1000.0
        if len(self.last_tick_ms) >= 60:
            self.last_tick_ms.pop(0)
        self.last_tick_ms.append(tick_ms)

        # always at the end
        self.entities.sort(key=lambda e: (e.LAYER_PRIORITY, e.depth_y))

    def audio(self, mixer):
        for entity in self.entities:
            entity.audio(mixer)

    def add_entity(self, entity):
        is_player = type(entity).__name__ == "Player"
       
        if is_player:
            self.player = entity
            self.entities.append(entity)
        else:
            if self.player in self.entities:
                player_index = self.entities.index(self.player)
                self.entities.insert(player_index, entity)
            else:
                self.entities.append(entity)


        if entity.physics.main_hitbox:
            self.solid_entities.append(entity)


    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
        if entity in self.solid_entities:
            self.solid_entities.remove(entity)
        if self.player == entity:
            self.player = None


    def _rebuild_spatial_grid(self):
        self.spatial_grid.clear()
        for entity in self.entities:
            self.spatial_grid.insert(entity)


    """
    def check_triggers_tick(self):
        checked_pairs = set()

        for entity_a in self.entities:
            if type(entity_a).__name__ != "Player":
                continue

            phys_a = entity_a.physics
            nearby = self.spatial_grid.get_nearby_entities(entity_a)

            for entity_b in nearby:
                pair_key = (
                    (id(entity_a), id(entity_b))
                    if id(entity_a) < id(entity_b)
                    else (id(entity_b), id(entity_a))
                )
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                phys_b = entity_b.physics

                for box_a in phys_a.hitboxes:
                    for box_b in phys_b.hitboxes:
                        if self.hitboxes_overlapping(box_a, phys_a, box_b, phys_b):
                            box_a.on_collide(box_b, entity_a, entity_b)
                            box_b.on_collide(box_a, entity_b, entity_a)
    """

    @staticmethod
    def hitboxes_overlapping(box_a: Hitbox, phys_a: EntityPhysics, box_b: Hitbox, phys_b: EntityPhysics) -> bool:
        pos_a = box_a.get_absolute_position(phys_a.position, phys_a.width, phys_a.height)
        pos_b = box_b.get_absolute_position(phys_b.position, phys_b.width, phys_b.height)

        # --- RECTANGLE vs RECTANGLE ---
        if box_a.type == HitboxType.RECTANGLE and box_b.type == HitboxType.RECTANGLE:
            return (pos_a.x < pos_b.x + box_b.w_or_r and
                    pos_a.x + box_a.w_or_r > pos_b.x and
                    pos_a.y < pos_b.y + box_b.height and
                    pos_a.y + box_a.height > pos_b.y)
            
        # --- CIRCLE vs CIRCLE ---
        if box_a.type == HitboxType.CIRCLE and box_b.type == HitboxType.CIRCLE:
            return (pos_a - pos_b).length_squared() < (box_a.w_or_r + box_b.w_or_r) ** 2
        
        # --- CIRCLE vs RECTANGLE ---
        if (box_a.type == HitboxType.CIRCLE and box_b.type == HitboxType.RECTANGLE) or \
           (box_a.type == HitboxType.RECTANGLE and box_b.type == HitboxType.CIRCLE):
            
            if box_a.type == HitboxType.CIRCLE:
                c_center, r_tl = pos_a, pos_b
                circle_box, rect_box = box_a, box_b
            else:
                c_center, r_tl = pos_b, pos_a
                circle_box, rect_box = box_b, box_a
            
            radius = circle_box.w_or_r
            half_w = rect_box.w_or_r / 2.0
            half_h = rect_box.height / 2.0

            rect_center = r_tl + Vector2f(half_w, half_h)
            diff = c_center - rect_center
            dist_x = abs(diff.x)
            dist_y = abs(diff.y)

            if dist_x > (half_w + radius) or dist_y > (half_h + radius): 
                return False

            if dist_x <= half_w or dist_y <= half_h: 
                return True

            return (dist_x - half_w) ** 2 + (dist_y - half_h) ** 2 < radius ** 2

        return False

    def render(self, graphics: Renderer, camera: Camera = None):
        cam_left = camera.position.x
        cam_right = camera.position.x + camera.screen_width
        cam_top = camera.position.y
        cam_bottom = camera.position.y + camera.screen_height


        for entity in self.entities:
            phys = entity.physics
           
            half_w = phys.width / 2.0
            half_h = phys.height / 2.0
           
            entity_left = phys.position.x - half_w
            entity_right = phys.position.x + half_w
            entity_top = phys.position.y - half_h
            entity_bottom = phys.position.y + half_h


            if (entity_right < cam_left or
                entity_left > cam_right or
                entity_bottom < cam_top or
                entity_top > cam_bottom):
                continue


            entity.render(graphics, camera)