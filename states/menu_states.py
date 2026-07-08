from states.base_state import State
from ui.button import Button
from states.manager import StateManager
from states.game_states import GameState, WorldState
from states.editor_states import EditorState

class MenuState(State):
    def __init__(self, manager: StateManager):
        super().__init__(manager)

    def player_input(self, inputs):
        pass
    
    def tick(self, dt):
        pass

    def render(self, graphics):
        pass

class MainMenuState(State):
    def __init__(self, manager):
        super().__init__(manager)

        self.level_select_btn = Button(50, 200, 100, 50, 
                                    "LEVEL SELECT", 
                                    on_click=self.level_select,
                                    on_hover=lambda: setattr(self.level_select_btn, "color", (150, 50, 50))
                                       )

        self.objects.append(self.level_select_btn)

    def player_input(self, inputs):
        super().player_input(inputs)
    
    def tick(self, dt):
        super().tick(dt)

    def render(self, graphics):
        super().render(graphics)

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