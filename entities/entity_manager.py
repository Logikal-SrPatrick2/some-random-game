from entities.hitbox import Hitbox, HitboxType
from entities.spatial_grid import SpatialGrid
from graphics.renderer import Renderer
from graphics.camera import Camera


class EntityManager:
    def __init__(self):
        self.entities = []
        self.solid_entities = []
        self.player = None
        self.spatial_grid = SpatialGrid()


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


    def check_triggers_tick(self):
        checked_pairs = set()

        for entity_a in self.entities:
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
                        if self._hitboxes_overlapping(box_a, phys_a, box_b, phys_b):
                            box_a.on_collide(box_b, entity_a, entity_b)
                            box_b.on_collide(box_a, entity_b, entity_a)


    def _hitboxes_overlapping(self, box_a, phys_a, box_b, phys_b) -> bool:
        tl_a = box_a.get_absolute_position(phys_a.position, phys_a.width, phys_a.height)
        tl_b = box_b.get_absolute_position(phys_b.position, phys_b.width, phys_b.height)


        if box_a.type == HitboxType.RECTANGLE and box_b.type == HitboxType.RECTANGLE:
            return (tl_a.x < tl_b.x + box_b.w_or_r and
                    tl_a.x + box_a.w_or_r > tl_b.x and
                    tl_a.y < tl_b.y + box_b.height and
                    tl_a.y + box_a.height > tl_b.y)
           
        elif box_a.type == HitboxType.CIRCLE and box_b.type == HitboxType.CIRCLE:
            center_a = phys_a.position + box_a.offset
            center_b = phys_b.position + box_b.offset
            dist_sq = (center_a.x - center_b.x)**2 + (center_a.y - center_b.y)**2
            return dist_sq < (box_a.w_or_r + box_b.w_or_r)**2
       
        elif (box_a.type == HitboxType.CIRCLE and box_b.type == HitboxType.RECTANGLE) or \
             (box_a.type == HitboxType.RECTANGLE and box_b.type == HitboxType.CIRCLE):
           
            circle_box, rect_box = (box_a, box_b) if box_a.type == HitboxType.CIRCLE else (box_b, box_a)
            c_phys, r_phys = (phys_a, phys_b) if box_a.type == HitboxType.CIRCLE else (phys_b, phys_a)
           
            c_center = c_phys.position + circle_box.offset
            r_tl = rect_box.get_absolute_position(r_phys.position, r_phys.width, r_phys.height)
           
            closest_x = max(r_tl.x, min(c_center.x, r_tl.x + rect_box.w_or_r))
            closest_y = max(r_tl.y, min(c_center.y, r_tl.y + rect_box.height))
           
            distance_sq = (c_center.x - closest_x)**2 + (c_center.y - closest_y)**2
            return distance_sq < (circle_box.w_or_r)**2


        return False


    def player_input(self, inputs):
        for entity in self.entities:
            entity.player_input(inputs)


    def tick(self, dt: float):
        self._rebuild_spatial_grid()
        self.check_triggers_tick()


        for entity in self.entities:
            entity.tick(dt)


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