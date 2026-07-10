import pygame
from utils.conversion_to_exe import resource_path

class AudioAsset:
    sfx_cache = {}
    bgm_paths = {}

    @classmethod
    def load_all_assets(cls):
        print("Loading audio assets into RAM...")
        
        # SFX (.wav) -> RAM for instant playback
        cls.sfx_cache["plasma_bullet"] = pygame.mixer.Sound(resource_path("res/audio/sfx/SFX1PLASMABULLET.wav"))
        
        # BGM (.mp3)
        cls.bgm_paths["main_menu"] = resource_path("res/audio/bgm/OST1MAINMENU.mp3")
        cls.bgm_paths["world"] = resource_path("res/audio/bgm/OST2WORLD.mp3")