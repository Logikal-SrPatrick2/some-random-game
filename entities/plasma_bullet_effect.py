from entities.entity import Entity
from entities.entity_manager import EntityManager
from entities.entity_physics import EntityPhysics
from tiles.tile_manager import TileManager
from graphics.spritesheet import Spritesheet
from graphics.animation import Animation
from utils.conversion_to_exe import resource_path

class PlasmaBulletEffect(Entity):
    def __init__(self, manager: EntityManager, tile_manager: TileManager, x: int, y: int):
        self.physics = EntityPhysics(
            x,
            y,
            32,
            32
        )

        img_path = resource_path("res/spritesheets/plasma_bullet/plasma_bullet.png")
        json_path = resource_path("res/spritesheets/plasma_bullet/plasma_bullet.json")
        self.animation = Animation(Spritesheet(img_path, json_path).get_frames(), frame_duration_ms=50, loops=False)
        self.animation.resize(64, 64)

        super().__init__(self.physics, self.animation, manager, tile_manager)

    def tick(self, dt):
        super().tick(dt)

        if self.animation.done:
            self.manager.remove_entity(self)