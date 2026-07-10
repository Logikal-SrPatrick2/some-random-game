import json
import pygame
from graphics.image_asset import ImageAsset

class Spritesheet:
    def __init__(self, image_path, json_path):
        self.master_asset = ImageAsset(file_path=image_path)
        
        with open(json_path, 'r', encoding="utf-8") as f:
            self.data = json.load(f)

    def get_frames(self):
        frames_list = []
        
        for frame_name, frame_info in self.data["frames"].items():
            rect_data = frame_info["frame"]
            
            sub_rect = pygame.Rect(rect_data["x"], rect_data["y"], rect_data["w"], rect_data["h"])
            
            cropped_surface = self.master_asset.surface.subsurface(sub_rect)
            
            frames_list.append(ImageAsset(surface=cropped_surface))
            
        return frames_list