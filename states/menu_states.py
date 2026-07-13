from states.base_state import State
from ui.button import Button
from ui.main_button import MainButton
from states.manager import StateManager
from states.game_states import GameState, WorldState
from states.editor_states import EditorState
from graphics.image_asset import ImageAsset
from graphics.renderer import Renderer
from graphics.render_mode import RenderMode
from entities.utils.entity_manager import EntityManager
from tiles.tile_manager import TileManager
from world.level_io import LevelIO
from graphics.camera import Camera
from auditory.mixer import Mixer
from utils.conversion_to_exe import resource_path, check_if_exist, get_save_path
from ui.toast import Toast
import pygame

class MenuState(State):
    def __init__(self, manager: StateManager):
        super().__init__(manager)

    def player_input(self, inputs):
        pass
    
    def tick(self, dt):
        pass

    def audio(self, mixer):
        pass

    def render(self, graphics):
        pass

class MainMenuState(State):
    def __init__(self, manager):
        super().__init__(manager)

        """
        self.level_select_btn = Button(50, 200, 100, 50, 
                                    "LEVEL SELECT", 
                                    on_click=self.level_select,
                                    on_hover=lambda: setattr(self.level_select_btn, "color", (150, 50, 50))
                                       )
        """

        self.tile_manager = TileManager()
        self.entity_manager = EntityManager()

        LevelIO.load_level("main_menu.json", self.tile_manager, self.entity_manager)

        self.camera = Camera(1280, 720)
        self.objects.append(self.tile_manager)
        self.objects.append(self.entity_manager)

        self.title = ImageAsset(resource_path("res/spritesheets/title/title.png"))
        self.title.resize(260*4, 39*4)

        self.play_btn = MainButton(
            1280//2, 720//4 + 150, 180*2, 36*2, "FREE PLAY", 0, 1, on_click=self.free_play
        )

        self.edit_btn = MainButton(
            1280//2, 720//4 + 250, 180*2, 36*2, "EDIT LEVEL", 0, 1, on_click=self.edit_custom
        )

        self.play_custom_btn = MainButton(
            1280//2, 720//4 + 350, 180*2, 36*2, "PLAY LEVEL", 0, 1, on_click=self.play_custom
        )

        self.exit_btn = MainButton(
            1280//2, 720//4 + 450, 180*2, 36*2, "EXIT", 0, 1, on_click=self.exit
        )

        self.toast = Toast()

        self.ui_elements.append(self.play_btn)
        self.ui_elements.append(self.edit_btn)
        self.ui_elements.append(self.play_custom_btn)
        self.ui_elements.append(self.exit_btn)
        self.ui_elements.append(self.toast)

        self.bgm_is_playing = False

    def player_input(self, inputs):
        super().player_input(inputs)
    
    def tick(self, dt):
        super().tick(dt)

    def audio(self, mixer: Mixer):
        super().audio(mixer)
        if not self.bgm_is_playing:
            mixer.play_music("main_menu")
            self.bgm_is_playing = True
            print("MAIN MENU MUSIC PLAYING")

    def render(self, graphics: Renderer):
        super().render(graphics)
        self.title.render(graphics, 1280//2, 720//10 + 50, RenderMode.CENTER)
        graphics.draw_text_centered("By: Patrick & Meakay", (92, 225, 230), 1280//2 - 415, 720//10 + 150, customFont=graphics.orbitron)
        graphics.draw_text_centered("Pre-Alpha v0.3.2", (92, 225, 230), 1280//2 + 395, 720//10 + 150, customFont=graphics.orbitron)

    def free_play(self):
        self.manager.change_state(GameState(self.manager))
        self.manager.push(WorldState(self.manager, "free_play.json"))

    def edit_custom(self):
        self.manager.change_state(EditorState(self.manager, 1280, 720))

    def play_custom(self):
        if check_if_exist(get_save_path("levels/edit_level.json")):
            self.manager.change_state(GameState(self.manager))
            self.manager.push(WorldState(self.manager, "edit_level.json"))
        else:
            self.toast.execute_toast("PLEASE CREATE A LEVEL FIRST", 60, 1000)

    def exit(self):
        from systems.activation import kill_program
        kill_program()

    def level_select(self):
        self.manager.push(LevelSelectState(self.manager))

class LevelSelectState(State):
    def __init__(self, manager):
        super().__init__(manager)

        self.back_btn = Button(400, 500, 100, 50, 
                            "BACK", 
                            on_click=self.back_to_main,
                            on_hover=lambda: setattr(self.back_btn, "color", (150, 50, 50))
                                )
        
        self.free_play_btn = Button(400, 300, 100, 50, 
                            "NEW GAME", 
                            on_click=self.free_play,
                            on_hover=lambda: setattr(self.free_play_btn, "color", (150, 50, 50))
                                )
        
        self.edit_btn = Button(400, 400, 100, 50, 
                            "EDIT LEVEL", 
                            on_click=self.open_editor,
                            on_hover=lambda: setattr(self.edit_btn, "color", (150, 50, 50))
                                )
        
        self.custom_level_btn = Button(520, 400, 100, 50, 
                            "PLAY CUSTOM LVL", 
                            on_click=self.custom_level,
                            on_hover=lambda: setattr(self.custom_level_btn, "color", (150, 50, 50))
                                )
        
        self.objects.append(self.back_btn)
        self.objects.append(self.free_play_btn)
        self.objects.append(self.edit_btn)
        self.objects.append(self.custom_level_btn)
    
    def player_input(self, inputs):
        super().player_input(inputs)

    def tick(self, dt):
        super().tick(dt)

    def render(self, graphics):
        graphics.draw_rect(300, 300, 400, 300, (200, 200, 255))
        super().render(graphics)

    def back_to_main(self):
        self.manager.pop()

    def free_play(self):
        self.manager.change_state(GameState(self.manager))
        self.manager.push(WorldState(self.manager, "free_play.json"))

    def custom_level(self):
        self.manager.change_state(GameState(self.manager))
        self.manager.push(WorldState(self.manager, "edit_level.json"))

    def open_editor(self):
        self.manager.change_state(EditorState(self.manager, 1280, 720))

class OptionsState(State):
    pass

class CreditsState(State):
    pass