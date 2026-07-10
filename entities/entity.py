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

class Entity:
    def __init__(self, physics_component: EntityPhysics, animation_component: Animation, manager: EntityManager, tile_manager: TileManager):
        self.physics = physics_component
        self.animation = animation_component
        self.manager = manager
        self.tile_manager = tile_manager

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