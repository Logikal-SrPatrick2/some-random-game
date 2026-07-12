from entities.creature import Creature
from entities.entity_physics import EntityPhysics
from entities.hitbox import Hitbox, HitboxType
from entities.entity_manager import EntityManager
from graphics.animation import Animation
from graphics.spritesheet import Spritesheet
from graphics.renderer import Renderer
from graphics.render_mode import RenderMode
from utils.conversion_to_exe import resource_path
from tiles.tile_manager import TileManager

DEFAULT_HEALTH = 40
DEFAULT_IDLE_SPRITE_FRAME_SPEED = 200 #ms
DEFAULT_SPRITE_RESIZE = 128 # 32 times 4

class RoamingAlien(Creature):
    def __init__(self, manager: EntityManager, tile_manager: TileManager, x, y, width, height):
        self.physics = EntityPhysics(
            x=x,
            y=y,
            width=width,
            height=height,
            vx=0,
            vy=0,
            ax=0,
            ay=0
        )

        self.name = "RoamingAlien"

        self.physics.add_hitbox(
            Hitbox(
                "ROAMING ALIEN HITBOX",
                HitboxType.RECTANGLE,
                45,
                32,
                38,
                64,
                True
            ),
            True
        )

        img_path = resource_path("res/spritesheets/roaming_alien/roaming_alien.png")
        json_path = resource_path("res/spritesheets/roaming_alien/roaming_alien.json")

        master_spritesheet = Spritesheet(img_path, json_path).get_frames()
        self.animation = Animation(master_spritesheet, frame_duration_ms=DEFAULT_IDLE_SPRITE_FRAME_SPEED)
        self.animation.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)

        super().__init__(self.physics, self.animation, manager, tile_manager, DEFAULT_HEALTH)

        self.max_speed = 200.0

    def tick(self, dt):
        self.pathfind_tick(dt, self.manager.player)
        super().tick(dt)

    def render(self, graphics, camera, mode = RenderMode.CENTER):
        super().render(graphics, camera, mode)