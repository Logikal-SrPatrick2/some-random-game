from graphics.image_asset import ImageAsset
from graphics.animation import Animation
from graphics.spritesheet import Spritesheet
from utils.conversion_to_exe import resource_path

__ROAMING_ALIEN_APPROACH_SPRITESHEET = Spritesheet(
    resource_path(
        "res/spritesheets/roaming_alien/meakay_alien/Roaming_Alien_Animation/Roaming_Alien_Animation.png"
    ),
    resource_path(
        "res/spritesheets/roaming_alien/meakay_alien/Roaming_Alien_Animation/Roaming_Alien_Animation.json"
    )
)


def get_roaming_alien_approach() -> Animation:
    return Animation(__ROAMING_ALIEN_APPROACH_SPRITESHEET.get_frames(), 500)

def get_roaming_idle_image() -> ImageAsset:
    return __ROAMING_ALIEN_APPROACH_SPRITESHEET.get_frames()[0]

__ROAMING_ALIEN_ATTACK_SPRITESHEET = Spritesheet(
    resource_path(
        "res/spritesheets/roaming_alien/meakay_alien/Roaming_Alien_Attack/Roaming_Alien_Attack.png"
    ),
    resource_path(
        "res/spritesheets/roaming_alien/meakay_alien/Roaming_Alien_Attack/Roaming_Alien_Attack.json"
    )
)


def get_roaming_alien_attack() -> Animation:
    return Animation(__ROAMING_ALIEN_ATTACK_SPRITESHEET.get_frames(), 111)