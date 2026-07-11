from entities.creature import Creature
from entities.entity_physics import EntityPhysics
from entities.hitbox import Hitbox, HitboxType
from entities.entity_manager import EntityManager
from graphics.animation import Animation
from graphics.spritesheet import Spritesheet
from systems.input_handler import InputHandler
from tiles.tile_manager import TileManager
from utils.vector2f import Vector2f
from entities.plasma_bullet_effect import PlasmaBulletEffect
from auditory.mixer import Mixer
from random import randrange
from utils.conversion_to_exe import resource_path
import pygame

DEFAULT_HEALTH = 100
DEFAULT_ATTACK_COOLDOWN = 500 #ms
DEFAULT_DMG = 20
DEFAULT_WALK_VELOCITY = 300
DEFAULT_SPRITE_RESIZE = 128 # 32 times 4
DEFAULT_WALK_SPRITE_FRAME_SPEED = 200 #ms
DEFAULT_ATTACK_RADIUS = 384

class Player(Creature):
    def __init__(self, manager: EntityManager, tile_manager: TileManager, x: float, y: float, width: int, height: int):
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

        self.name = "Player"

        self.physics.add_hitbox(
            Hitbox(
                "PLAYER HITBOX",
                HitboxType.RECTANGLE,
                48,
                48,
                32,
                80,
                True
            ),
            True
        )

        self.physics.add_hitbox(
            Hitbox(
                "ATTACK RANGE",
                HitboxType.CIRCLE,
                64,
                128,
                DEFAULT_ATTACK_RADIUS,
                on_collide_callback=self.range_hitbox_on_collide
            )
        )

        self.creatures_within_attack_range = set()
        self.creatures_within_attack_range_temp = set()
        self.closest_creature = None

        img_path = resource_path("res/spritesheets/player/player.png")
        json_path = resource_path("res/spritesheets/player/player.json")
        master_spritesheet = Spritesheet(img_path, json_path)
        all_frames = master_spritesheet.get_frames()

        self.idle_img = all_frames[0]
        self.walk_right = Animation(all_frames[1:4] + [all_frames[2]], frame_duration_ms=DEFAULT_WALK_SPRITE_FRAME_SPEED)
        self.walk_left  = Animation(all_frames[4:7] + [all_frames[5]], frame_duration_ms=DEFAULT_WALK_SPRITE_FRAME_SPEED)
        self.walk_front = Animation(all_frames[7:10] + [all_frames[8]], frame_duration_ms=DEFAULT_WALK_SPRITE_FRAME_SPEED)
        self.walk_back  = Animation(all_frames[10:13] + [all_frames[11]], frame_duration_ms=DEFAULT_WALK_SPRITE_FRAME_SPEED)
        self.plasma_p17_right = all_frames[13]
        self.plasma_p17_left = all_frames[14]

        self.idle_img.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.walk_right.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.walk_left.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.walk_front.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.walk_back.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.plasma_p17_right.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.plasma_p17_left.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)

        super().__init__(self.physics, self.idle_img, manager, tile_manager, DEFAULT_HEALTH, DEFAULT_ATTACK_COOLDOWN, DEFAULT_DMG)

        self.is_shooting = False
        self.play_shooting_sound = False
        self.on_successful_attack_callback = self.on_successful_attack

    def player_input(self, inputs: InputHandler):
        super().player_input(inputs)

        if inputs.keys[pygame.K_SPACE]:
            self.attack(self.closest_creature)
            self.physics.velocity.x = 0.0
            self.physics.velocity.y = 0.0
            self.is_shooting = True
        else:
            self.is_shooting = False
            if inputs.keys[pygame.K_d] and inputs.keys[pygame.K_a]:
                self.physics.velocity.x = 0.0
            else:
                if inputs.keys[pygame.K_d]:
                    self.physics.velocity.x = DEFAULT_WALK_VELOCITY
                elif inputs.keys[pygame.K_a]:
                    self.physics.velocity.x = -DEFAULT_WALK_VELOCITY
                else:
                    self.physics.velocity.x = 0.0

            if inputs.keys[pygame.K_s] and inputs.keys[pygame.K_w]:
                self.physics.velocity.y = 0.0
            else:
                if inputs.keys[pygame.K_s]:
                    self.physics.velocity.y = DEFAULT_WALK_VELOCITY
                elif inputs.keys[pygame.K_w]:
                    self.physics.velocity.y = -DEFAULT_WALK_VELOCITY
                else:
                    self.physics.velocity.y = 0.0

    def tick(self, dt):
        super().tick(dt) 
        self.creatures_within_attack_range = self.creatures_within_attack_range_temp.copy()

        if self.creatures_within_attack_range_temp:
            self.creatures_within_attack_range_temp.clear()

        if self.creatures_within_attack_range:
            new_closest_creature = min(
                self.creatures_within_attack_range,
                key=lambda c: Vector2f.distance(self.physics.position, c.physics.position)
            )

            if not self.closest_creature is new_closest_creature:
                if self.closest_creature:
                    self.closest_creature.physics.main_hitbox.show_hitbox = False
                self.closest_creature = new_closest_creature
                self.closest_creature.physics.main_hitbox.show_hitbox = True
        else:
            if self.closest_creature:
                self.closest_creature.physics.main_hitbox.show_hitbox = False
                self.closest_creature = None

        if self.is_shooting:
            if self.closest_creature:
                if self.closest_creature.physics.position.x > self.physics.position.x:
                    self.animation = self.plasma_p17_right
                else:
                    self.animation = self.plasma_p17_left
            else: 
                self.animation = self.plasma_p17_right
        else:
            if self.physics.velocity.is_zero:
                self.animation = self.idle_img
            else:
                if self.physics.velocity.y > 0:
                    self.animation = self.walk_front
                elif self.physics.velocity.y < 0:
                    self.animation = self.walk_back 
                elif self.physics.velocity.x > 0:
                    self.animation = self.walk_right 
                elif self.physics.velocity.x < 0:
                    self.animation = self.walk_left 

    def audio(self, mixer: Mixer):
        super().audio(mixer)

        if self.play_shooting_sound:
            mixer.play_sfx("plasma_bullet")
            self.play_shooting_sound = False

    def render(self, graphics, camera):
        super().render(graphics, camera)

    def range_hitbox_on_collide(self, _, player, entity_in_range):
        self.creatures_within_attack_range_temp.add(entity_in_range)

    def on_successful_attack(self):
        hitbox_abs = self.closest_creature.physics.main_hitbox.get_absolute_position(self.closest_creature.physics.position, self.closest_creature.physics.width, self.closest_creature.physics.height)
        x = hitbox_abs.x
        y = hitbox_abs.y
        w = self.closest_creature.physics.main_hitbox.w_or_r
        h = self.closest_creature.physics.main_hitbox.height
        effect_x = randrange(int(x), int(x + w))
        effect_y = randrange(int(y), int(y + h))
        self.manager.add_entity(PlasmaBulletEffect(self.manager, self.tile_manager, effect_x, effect_y))
        self.play_shooting_sound = True
