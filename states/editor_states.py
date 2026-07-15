import pygame
from states.manager import StateManager
from states.base_state import State
from graphics.camera import Camera
from utils.vector2f import Vector2f
from tiles.tile_manager import TileManager, TILE_FACTORY
from tiles.base_tile import DEFAULT_TILE_SIZE
from tiles.tile_types import FloorPlain
from tiles import TILE_IMAGE_ASSETS
from world.level_io import LevelIO
from ui.palette_panel import PalettePanel
from ui.button import Button
from entities.utils.entity_manager import EntityManager
from entities.mechanics.entity_physics import EntityPhysics
from utils.conversion_to_exe import check_if_exist, get_save_path
from ui.toast import Toast
from systems.input_handler import InputHandler

class EditorState(State):
    editor_filename = "edit_level.json"

    def __init__(self, manager: StateManager, screen_width: int, screen_height: int, 
                 entity_manager: EntityManager = None, tile_manager: TileManager = None):
        super().__init__(manager)
        self.camera = Camera(screen_width, screen_height)

        self.toast = Toast()
        
        self.entity_manager = entity_manager if entity_manager is not None else EntityManager()
        self.tile_manager = tile_manager if tile_manager is not None else TileManager()
        
        default_map = [[0] * 32 for _ in range(32)]
        self.tile_manager.load_map(default_map)
        
        # UI Sidebar Panel Configuration
        self.palette = PalettePanel(screen_width - 400, 0, 400, screen_height)
        
        self.save_btn = Button(10, 10, 140, 35, "Save JSON", on_click=self.trigger_save)
        self.load_btn = Button(160, 10, 140, 35, "Load JSON", on_click=self.trigger_load)
        self.menu_btn = Button(310, 10, 150, 35, "Return to Menu", on_click=self.return_to_menu)
        
        self.cam_speed = 500.0  # Pixels per second free-roaming speed

    def select_player_brush(self):
        self.palette.active_brush_type = "ENTITY"
        self.palette.active_id = "Player"
        print("[EDITOR] Active brush set to: Player")

    def player_input(self, inputs: InputHandler):
        dt = 1.0 / 60.0
        
        move_dir = Vector2f(0.0, 0.0)
        if inputs.keys[pygame.K_w] or inputs.keys[pygame.K_UP]:    move_dir.y -= 1
        if inputs.keys[pygame.K_s] or inputs.keys[pygame.K_DOWN]:  move_dir.y += 1
        if inputs.keys[pygame.K_a] or inputs.keys[pygame.K_LEFT]:  move_dir.x -= 1
        if inputs.keys[pygame.K_d] or inputs.keys[pygame.K_RIGHT]: move_dir.x += 1
        
        if not move_dir.is_zero:
            self.camera.position += move_dir.normalize() * self.cam_speed * dt

        self.palette.player_input(inputs)
        self.save_btn.player_input(inputs)
        self.load_btn.player_input(inputs)
        self.menu_btn.player_input(inputs)

        if inputs.mouse_pos[0] < self.palette.rect.x:
            world_mouse_x = inputs.mouse_pos[0] + self.camera.position.x
            world_mouse_y = inputs.mouse_pos[1] + self.camera.position.y
            
            grid_x = int(world_mouse_x // DEFAULT_TILE_SIZE)
            grid_y = int(world_mouse_y // DEFAULT_TILE_SIZE)
            
            if 0 <= grid_x < self.tile_manager.cols and 0 <= grid_y < self.tile_manager.rows:
                if self.palette.active_brush_type == "ENTITY":
                    if inputs.mouse_clicked[0]:    # Left Click - Paint Item
                        self.execute_placement(grid_x, grid_y, world_mouse_x, world_mouse_y)
                    elif inputs.mouse_clicked[2]:  # Right Click - Erase Brush
                        self.execute_tile_paint(grid_x, grid_y, 0)
                else:
                    if inputs.mouse_buttons[0]:    # Left Click - Paint Item
                        self.execute_placement(grid_x, grid_y, world_mouse_x, world_mouse_y)
                    elif inputs.mouse_buttons[2]:  # Right Click - Erase Brush
                        self.execute_tile_paint(grid_x, grid_y, 0)

    def execute_tile_paint(self, grid_x, grid_y, tile_id):
        tile_class = TILE_FACTORY.get(tile_id, FloorPlain)
        new_tile = tile_class(grid_x, grid_y)
        
        if 0 <= new_tile.id < len(TILE_IMAGE_ASSETS):
            new_tile.graphics_asset = TILE_IMAGE_ASSETS[new_tile.id]
            
        self.tile_manager.tilemap[grid_y][grid_x] = new_tile

    def execute_placement(self, grid_x, grid_y, world_x, world_y):
        if self.palette.active_brush_type == "TILE":
            tile_id = int(self.palette.active_id) if self.palette.active_id is not None else 0
            self.execute_tile_paint(grid_x, grid_y, tile_id)
            
        elif self.palette.active_brush_type == "ENTITY":
            ent_type = self.palette.active_id  # Expected String value: "Player" or "RoamingAlien"
            if not ent_type:
                return
                
            if ent_type == "Player":
                self.entity_manager.entities = [
                    ent for ent in self.entity_manager.entities 
                    if ent.name != "Player"
                ]

            mock_attrs = {"x": world_x, "y": world_y, "width": 128, "height": 128}
            
            class MockEditorEntity:
                def __init__(self, name, attrs):
                    self.name = name
                    self.physics = EntityPhysics(
                        x=attrs["x"],
                        y=attrs["y"],
                        width=attrs["width"],
                        height=attrs["height"]
                    )
            
            self.entity_manager.entities.append(MockEditorEntity(ent_type, mock_attrs))

        elif self.palette.active_brush_type == "DELETE_ENTITY":
            click_radius = 24
            self.entity_manager.entities = [
                ent for ent in self.entity_manager.entities
                if ((ent.physics.position.x - world_x) ** 2 + (ent.physics.position.y - world_y) ** 2) > click_radius ** 2
            ]

    def tick(self, dt):
        self.palette.tick(dt)
        self.save_btn.tick(dt)
        self.load_btn.tick(dt)
        self.menu_btn.tick(dt)
        self.tile_manager.tick(dt)
        self.toast.tick(dt)

    def render(self, graphics):
        self.tile_manager.render(graphics, self.camera)
        
        for ent in self.entity_manager.entities:
            screen_pos_x = ent.physics.position.x - self.camera.position.x
            screen_pos_y = ent.physics.position.y - self.camera.position.y
            
            ent_name = getattr(ent, "name", type(ent).__name__)
            
            if ent_name == "Player":
                dot_color = (0, 255, 0)
                display_name = "Player"
            else:
                dot_color = (255, 0, 0)
                display_name = "Alien"
            
            graphics.draw_circle_hollow(screen_pos_x, screen_pos_y, radius=12, color=dot_color, thickness=4)
            graphics.draw_text_centered(display_name, (255, 255, 255), int(screen_pos_x), int(screen_pos_y) - 25)
            
        self.palette.render(graphics)
        self.save_btn.render(graphics)
        self.load_btn.render(graphics)
        self.menu_btn.render(graphics)
        self.toast.render(graphics)
            
    def trigger_save(self):
        LevelIO.save_level(EditorState.editor_filename, self.tile_manager, self.entity_manager)
        print(f"Level saved to levels/{EditorState.editor_filename}")

    def trigger_load(self):
        if check_if_exist(get_save_path(f"levels/{EditorState.editor_filename}")):
            success = LevelIO.load_level(EditorState.editor_filename, self.tile_manager, self.entity_manager)
            if success:
                print("Level loaded successfully!")
        else:
            print("TOASTT")
            self.toast.execute_toast("PLEASE CREATE A LEVEL FIRST", 60, 1000)
            
    def return_to_menu(self):
        from states.menu_states import MenuState, MainMenuState
        self.manager.change_state(MenuState(self.manager))
        self.manager.push(MainMenuState(self.manager))