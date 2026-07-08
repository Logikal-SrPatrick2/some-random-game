from entities.creature import Creature
from entities.entity_physics import EntityPhysics
from entities.hitbox import Hitbox, HitboxType
from entities.entity_manager import EntityManager
from graphics.animation import Animation
from graphics.spritesheet import Spritesheet
from systems.input_handler import InputHandler
from tiles.tile_manager import TileManager
import pygame

DEFAULT_HEALTH = 100
DEFAULT_WALK_VELOCITY = 300
DEFAULT_SPRITE_RESIZE = 128 # 32 times 4
DEFAULT_WALK_SPRITE_FRAME_SPEED = 200 #ms

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

        img_path = "res/spritesheets/player/player.png"
        json_path = "res/spritesheets/player/player.json"
        master_spritesheet = Spritesheet(img_path, json_path)
        all_frames = master_spritesheet.get_frames()

        self.idle_img = all_frames[0]
        self.walk_right = Animation(all_frames[1:4] + [all_frames[2]], frame_duration_ms=DEFAULT_WALK_SPRITE_FRAME_SPEED)
        self.walk_left  = Animation(all_frames[4:7] + [all_frames[5]], frame_duration_ms=DEFAULT_WALK_SPRITE_FRAME_SPEED)
        self.walk_front = Animation(all_frames[7:10] + [all_frames[8]], frame_duration_ms=DEFAULT_WALK_SPRITE_FRAME_SPEED)
        self.walk_back  = Animation(all_frames[10:13] + [all_frames[11]], frame_duration_ms=DEFAULT_WALK_SPRITE_FRAME_SPEED)

        self.idle_img.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.walk_right.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.walk_left.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.walk_front.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)
        self.walk_back.resize(DEFAULT_SPRITE_RESIZE, DEFAULT_SPRITE_RESIZE)

        super().__init__(self.physics, self.idle_img, manager, tile_manager, DEFAULT_HEALTH)

    def player_input(self, inputs: InputHandler):
        super().player_input(inputs)

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
    def render(self, graphics, camera):
        super().render(graphics, camera)