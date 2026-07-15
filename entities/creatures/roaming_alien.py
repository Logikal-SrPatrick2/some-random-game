from entities.creatures.creature import Creature
from entities.mechanics.entity_physics import EntityPhysics
from entities.mechanics.hitbox import Hitbox, HitboxType
from entities.utils.entity_manager import EntityManager
from graphics.animation import Animation
from graphics.spritesheet import Spritesheet
from graphics.renderer import Renderer
from graphics.render_mode import RenderMode
from utils.conversion_to_exe import resource_path
from tiles.tile_manager import TileManager

DEFAULT_HEALTH = 40
DEFAULT_IDLE_SPRITE_FRAME_SPEED = 200 #ms
DEFAULT_SPRITE_RESIZE = 128 # 32 times 4
DEFAULT_DETECTION_RADIUS = 512

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

        self.detection_range_hitbox = Hitbox(
            "DETECTION RANGE HITBOX",
            HitboxType.CIRCLE,
            64,
            128,
            DEFAULT_DETECTION_RADIUS,
            on_collide_callback=self.approach_player
        )

        self.physics.add_hitbox(
            self.detection_range_hitbox
        )

        img_path = resource_path("res/spritesheets/roaming_alien/roaming_alien.png")
        json_path = resource_path("res/spritesheets/roaming_alien/roaming_alien.json")

        master_spritesheet = Spritesheet(img_path, json_path).get_frames()
        self.animation = Animation(master_spritesheet, frame_duration_ms=DEFAULT_IDLE_SPRITE_FRAME_SPEED)
        self.animation.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)

        super().__init__(self.physics, self.animation, manager, tile_manager, DEFAULT_HEALTH)

        self.max_speed = 200.0
        self.creatures_within_detection_range = set()
        self.creatures_within_detection_range_temp = set()

        self.player_detected = False

    def tick(self, dt):
        if self.player_detected:
            self.pathfind_tick(dt, self.manager.player)
            self.player_detected = False
        super().tick(dt)

        self.check_collisions_tick()

    def render(self, graphics, camera, mode = RenderMode.CENTER):
        super().render(graphics, camera, mode)

    def check_collisions_tick(self):
        if not self.manager.player:
            return
        player = self.manager.player
        phy: EntityPhysics = player.physics
        pbox: Hitbox = phy.main_hitbox
        if EntityManager.hitboxes_overlapping(self.detection_range_hitbox, self.physics, pbox, phy):
            self.detection_range_hitbox.on_collide(pbox, self, player)

    def approach_player(self, _, __, player):
        self.player_detected = True