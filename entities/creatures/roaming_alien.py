from entities.creatures.creature import Creature
from entities.mechanics.entity_physics import EntityPhysics
from entities.mechanics.hitbox import Hitbox, HitboxType
from entities.mechanics.raycast import RayCast
from entities.utils.entity_manager import EntityManager
from entities.indicators.spew import Spew
from graphics.animation import Animation
from graphics.spritesheet import Spritesheet
from graphics.renderer import Renderer
from graphics.render_mode import RenderMode
from utils.conversion_to_exe import resource_path
from tiles.tile_manager import TileManager
from utils.vector2f import Vector2f
from entities.creatures import get_roaming_alien_approach, get_roaming_alien_attack, get_roaming_idle_image

DEFAULT_HEALTH = 40
DEFAULT_SPRITE_RESIZE = 128 # 32 times 4
DEFAULT_DETECTION_RADIUS = 768
DEFAULT_ATTACK_COOLDOWN = 3000 #ms
DEFAULT_DMG = 15
DEFAULT_MAX_SPEED = 300.0

# attack phases
DEFAULT_ACTIVATE_SPEW = 1000 / 1000.0 #ms to s

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
                32,
                64,
                64,
                32,
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
        
        self.approach_anim: Animation = get_roaming_alien_approach()
        self.idle_img = get_roaming_idle_image()
        self.attack_anim = get_roaming_alien_attack()

        self.animation = self.idle_img
        super().__init__(self.physics, self.animation, manager, tile_manager, DEFAULT_HEALTH, DEFAULT_ATTACK_COOLDOWN, DEFAULT_DMG)

        self.max_speed = DEFAULT_MAX_SPEED
        self.creatures_within_detection_range = set()
        self.creatures_within_detection_range_temp = set()

        self.player_detected = False
        self.target_range = 128

        self.ready_spew = False
        self.angle_of_attack = 0

    def tick(self, dt):
        if self.time_accumulator >= self.attack_cooldown:
            self.freeze_movement = False

        if self.player_detected:
            reached_target = self.pathfind_tick(dt, self.manager.player)
            if reached_target:
                self.attack(self.manager.player)
            self.player_detected = False
        else:
            self.physics.velocity.set_zero()
        super().tick(dt)

        self.check_collisions_tick()

        # ATTACK PHASES
        if self.time_accumulator >= DEFAULT_ACTIVATE_SPEW and self.ready_spew:
            self.spew_attack()
            self.ready_spew = False

        # ANIMATIONS
        if self.player_detected and self.ready_spew and not self.animation is self.attack_anim:
            self.animation = self.attack_anim
            self.animation.reset()
        elif self.physics.velocity.is_zero and not self.animation is self.idle_img and not self.ready_spew:
            self.animation = self.idle_img
        elif not self.physics.velocity.is_zero and not self.animation is self.approach_anim and not self.ready_spew:
            self.animation = self.approach_anim
            self.animation.reset()

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

    def attack(self, creature):
        if self.time_accumulator >= self.attack_cooldown:
            self.angle_of_attack = int(Vector2f.angle_between_points(self.physics.position, self.manager.player.physics.position))

            self.manager.add_entity(Spew(self.manager, self.tile_manager, 
                                         self.physics.position.x, self.physics.position.y + 32, 
                                         self.angle_of_attack,
                                         self
                                         ))
            self.freeze_movement = True
            self.ready_spew = True
            self.time_accumulator -= self.attack_cooldown
            return True
        return False
    
    def spew_attack(self):
        sector_center = Vector2f(self.physics.position.x, self.physics.position.y + 32)
        player_phy: EntityPhysics = self.manager.player.physics
        p_pos = player_phy.position
        p_width = player_phy.width
        p_height = player_phy.height
        r_tl = player_phy.main_hitbox.get_absolute_position(p_pos, p_width, p_height)

        if player_phy.main_hitbox.check_sector_vs_box(sector_center, self.angle_of_attack, r_tl):
            player_center = player_phy.get_hitbox_center()
            my_center = self.physics.get_hitbox_center()
            if not RayCast.raycast_2d_solid_tile_detection(my_center, player_center, self.tile_manager):
                self.manager.player.damageCreature(self.dmg)
