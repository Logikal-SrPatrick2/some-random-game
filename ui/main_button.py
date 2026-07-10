import pygame
from graphics.spritesheet import Spritesheet
from graphics.image_asset import ImageAsset
from graphics.render_mode import RenderMode
from systems.input_handler import InputHandler
from graphics.renderer import Renderer

def get_spritesheet() -> list[ImageAsset]:
    img_path = "res/spritesheets/main_buttons/main_buttons.png"
    json_path = "res/spritesheets/main_buttons/main_buttons.json"
    btns_spritesheet = Spritesheet(img_path, json_path)

    return btns_spritesheet.get_frames()

class MainButton:
    images = get_spritesheet()
    SCALED_BUTTON_WIDTH = 200 * 2
    SCALED_BUTTON_HEIGHT = 56 * 2

    # centered ung gagamitin ko rito bahala na
    def __init__(self, x: int, y: int, width: int, height: int, text: str, unhover_index: int, hover_index: int = 0, on_click = None):
        self.img_unhover = MainButton.images[unhover_index]
        self.img_unhover.resize(MainButton.SCALED_BUTTON_WIDTH, MainButton.SCALED_BUTTON_HEIGHT)
        self.is_hovered = False
        self.text = text

        self.on_click_callback = on_click
        self.x = x
        self.y = y

        # centered
        self.rect = pygame.Rect(x - (width / 2), y - (height / 2), width, height)

        self.active_img = self.img_unhover
        self.text_color_unhover = (92, 225, 230)
        self.text_color_hover = (97, 39, 232)

        self.text_color = self.text_color_unhover

    def player_input(self, inputs: InputHandler):
        self.is_hovered = self.rect.collidepoint(inputs.mouse_pos)
    
        if self.is_hovered and inputs.mouse_clicked[0]:
            self._on_click()

    def tick(self, dt: float):
        if self.is_hovered:
            self.text_color = self.text_color_hover
        else:
            self.text_color = self.text_color_unhover

    def render(self, graphics: Renderer):
        self.active_img.render(graphics, self.x, self.y, RenderMode.CENTER)

        text_x = self.rect.x + (self.rect.width // 2)
        text_y = self.rect.y + (self.rect.height // 2)
        graphics.draw_text_centered(self.text, self.text_color, text_x, text_y, larger_font=True)

    def _on_click(self):
        if self.on_click_callback:
            self.on_click_callback()