from entities.entity import Entity
from entities.utils.entity_manager import EntityManager
from entities.mechanics.entity_physics import EntityPhysics
from graphics.renderer import Renderer
from graphics.camera import Camera
from tiles.tile_manager import TileManager

RADIUS = 256
DURATION_MS = 1000 #ms

class Spew(Entity):
    def __init__(self, manager: EntityManager, tile_manager: TileManager, x: int, y: int, angle: int, source_entity: Entity):
        self.physics = EntityPhysics(
            x,
            y,
            RADIUS,
            RADIUS
        )

        self.angle = angle
        self.duration = DURATION_MS / 1000.0
        self.source_entity = source_entity

        super().__init__(self.physics, None, manager, tile_manager)

        self.spew_timer_acc = 0.0

    def tick(self, dt):
        if self.source_entity not in self.manager.entities:
            self.manager.remove_entity(self)

        if self.spew_timer_acc < self.duration:
            self.spew_timer_acc += dt
        else:
            self.manager.remove_entity(self)

    def render(self, graphics: Renderer, camera: Camera):
        screen_center = camera.to_screen_coords(self.physics.position)

        graphics.draw_sector_standard(screen_center.x, screen_center.y, self.angle)