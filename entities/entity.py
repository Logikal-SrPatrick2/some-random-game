from __future__ import annotations
from entities.entity_physics import EntityPhysics
from graphics.animation import Animation
from graphics.render_mode import RenderMode
from graphics.renderer import Renderer
from graphics.camera import Camera
from entities.hitbox import Hitbox, HitboxType
from entities.entity_manager import EntityManager
from utils.vector2f import Vector2f
from tiles.tile_manager import TileManager
from auditory.mixer import Mixer
from entities.pathfinding import PathFinding

class Entity:
    def __init__(self, physics_component: EntityPhysics, animation_component: Animation, manager: EntityManager, tile_manager: TileManager):
        self.physics = physics_component
        self.animation = animation_component
        self.manager = manager
        self.tile_manager = tile_manager

        self.max_speed = 100.0 # default (px/s)

        # PATHFINDING
        self.pf = PathFinding(tile_manager)
        self.path_waypoints = []
        self.waypoint_threshold = 8.0 
        self.target_range = 64.0      
        self.path_timer = 0.0
        self.path_interval = 0.2      

    def pathfind_tick(self, dt: float, target_entity: Entity):
        if target_entity:
            self.path_timer += dt
            distance_to_player = (target_entity.physics.position - self.physics.position).length()

            if distance_to_player <= self.target_range:
                self.physics.velocity = Vector2f.zero()
                self.path_waypoints.clear()

            else:
                if self.path_timer >= self.path_interval:
                    self.path_timer = 0.0  # Reset timer
                    self.path_waypoints = self.pf.find_path(self.physics.position, target_entity.physics.position, self.physics)

                if self.path_waypoints:
                    target_node = self.path_waypoints[0]
                    displacement = target_node - self.physics.position
                    distance = displacement.length()

                    if distance <= self.waypoint_threshold:
                        self.path_waypoints.pop(0)
                        self.physics.velocity = Vector2f.zero()
                    else:
                        self.physics.velocity = displacement.normalize() * self.max_speed
                else:
                    self.physics.velocity = Vector2f.zero()

    def player_input(self, inputs):
        pass

    def tick(self, dt: float):
        self.physics.accelerate_tick(dt)
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
                debug_color = (255, 0, 0) # Red

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