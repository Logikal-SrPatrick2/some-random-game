from __future__ import annotations
from entities.mechanics.entity_physics import EntityPhysics
from graphics.animation import Animation
from graphics.render_mode import RenderMode
from graphics.renderer import Renderer
from graphics.camera import Camera
from entities.mechanics.hitbox import Hitbox, HitboxType
from entities.utils.entity_manager import EntityManager
from utils.vector2f import Vector2f
from tiles.tile_manager import TileManager
from auditory.mixer import Mixer
from entities.mechanics.pathfinding import PathFinding
import pygame

class Entity:
    LAYER_PRIORITY = 2

    def __init__(self, physics_component: EntityPhysics, animation_component: Animation, manager: EntityManager, tile_manager: TileManager):
        self.physics = physics_component
        self.animation = animation_component
        self.manager = manager
        self.tile_manager = tile_manager

        self.freeze_movement = False

        self.max_speed = 100.0 # default (px/s)

        # PATHFINDING
        self.pf = PathFinding(tile_manager)
        self.path_waypoints = []
        self.waypoint_threshold = 8.0 
        self.target_range = 64.0      
        self.path_timer = 0.0
        self.path_interval = 0.2

        # Y-DEPTH
        self.pivot_offset_y = 0 # start at zero
        self.update_pivot_y()

    def check_collisions_tick(self):
        pass      

    def pathfind_tick(self, dt: float, target_entity: Entity) -> bool:
        if not target_entity:
            self.physics.velocity = Vector2f.zero()
            return False

        self.path_timer += dt

        target_hitbox = target_entity.physics.main_hitbox
        target_main_hitbox_tl = target_hitbox.get_absolute_position(
            target_entity.physics.position,
            target_entity.physics.width,
            target_entity.physics.height
        )
        target_main_hitbox_center = target_main_hitbox_tl + Vector2f(
            target_hitbox.w_or_r / 2.0,
            target_hitbox.height / 2.0
        )

        self_hitbox = self.physics.main_hitbox
        main_hitbox_tl = self_hitbox.get_absolute_position(
            self.physics.position,
            self.physics.width,
            self.physics.height
        )
        main_hitbox_center = main_hitbox_tl + Vector2f(
            self_hitbox.w_or_r / 2.0,
            self_hitbox.height / 2.0
        )

        to_target = target_main_hitbox_center - main_hitbox_center
        dist_to_target_sq = to_target.length_squared()

        if dist_to_target_sq <= (self.target_range ** 2):
            self.physics.velocity = Vector2f.zero()
            self.path_waypoints.clear()
            return True   # <-- genuine "reached" signal

        if self.path_timer >= self.path_interval:
            self.path_timer = 0.0
            self.path_waypoints = self.pf.find_path(main_hitbox_center, target_main_hitbox_center, self.physics)

        if self.path_waypoints:
            target_node = self.path_waypoints[0]
            displacement = target_node - main_hitbox_center
            dist_to_node_sq = displacement.length_squared()

            if dist_to_node_sq <= (self.waypoint_threshold ** 2):
                self.path_waypoints.pop(0)
                if self.path_waypoints:
                    target_node = self.path_waypoints[0]
                    displacement = target_node - main_hitbox_center
                    self.physics.velocity = displacement.normalize() * self.max_speed
                else:
                    self.physics.velocity = Vector2f.zero()
            else:
                self.physics.velocity = displacement.normalize() * self.max_speed
        else:
            self.physics.velocity = Vector2f.zero()   # not reached, just no path yet

        return False

    def player_input(self, inputs):
        pass

    def tick(self, dt: float):
        self.physics.accelerate_tick(dt)
        if not self.freeze_movement:
            self.physics.movement_tick(dt, self.manager, self.tile_manager, self)
        self.animation.tick(dt)

    def audio(self, mixer: Mixer):
        pass

    def render(self, graphics: Renderer, camera: Camera, mode: RenderMode = RenderMode.CENTER):
        screen_center = camera.to_screen_coords(self.physics.position)

        self.animation.render(
            graphics, 
            screen_center.x, 
            screen_center.y, 
            mode
        )
        
        for hitbox in self.physics.hitboxes:
            if hitbox.show_hitbox:
                debug_color = (255, 255, 127)

                tl_coords = hitbox.get_absolute_position(self.physics.position, self.physics.width, self.physics.height)
                screen_hitbox = camera.to_screen_coords(tl_coords)
                    
                screen_hitbox_x = screen_hitbox.x
                screen_hitbox_y = screen_hitbox.y
                
                if hitbox.type == HitboxType.RECTANGLE:
                    graphics.draw_rect_hollow(
                        int(round(screen_hitbox_x)), 
                        int(round(screen_hitbox_y)), 
                        int(round(hitbox.w_or_r)), 
                        int(round(hitbox.height)), 
                        debug_color
                    )
                    
                elif hitbox.type == HitboxType.CIRCLE:
                    graphics.draw_circle_hollow(
                        int(round(screen_hitbox_x)), 
                        int(round(screen_hitbox_y)), 
                        int(round(hitbox.w_or_r)), 
                        debug_color
                    )

    def update_pivot_y(self):
        if self.animation:
            self.pivot_offset_y = self.animation.calculate_auto_pivot

    @property
    def depth_y(self) -> int:
        return int(self.physics.position.y + self.pivot_offset_y)