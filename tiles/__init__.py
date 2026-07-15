from utils.conversion_to_exe import resource_path
from graphics.spritesheet import Spritesheet
from graphics.image_asset import ImageAsset
import os

BASE_FLOOR_PATH = resource_path("res\spritesheets\\tilemap\meakay_tiles\Floor")
BASE_WALL_PATH = resource_path("res\spritesheets\\tilemap\meakay_tiles\Wall")

TILE_IMAGE_ASSETS: list[ImageAsset] = []

FLOOR_LIST = ['Tile_Plain 1.0', 'Tile_Edge_Down', 'Tile_Edge_Left', 'Tile_Edge_Left-Down', 'Tile_Edge_Left-Up', 'Tile_Edge_Right', 'Tile_Edge_Right-Down', 'Tile_Edge_Right-Up', 'Tile_Edge_Up']
for floor_name in FLOOR_LIST:
    img_name = floor_name + ".png"
    json_name = floor_name + ".json"

    img_path = os.path.join(BASE_FLOOR_PATH, floor_name, img_name)
    json_path = os.path.join(BASE_FLOOR_PATH, floor_name, json_name)

    floor_sprite = Spritesheet(img_path, json_path)
    TILE_IMAGE_ASSETS.append(floor_sprite.get_frames()[0])

#print([entry.name for entry in os.scandir(BASE_WALL_PATH) if entry.is_dir()])

WALL_BACK_BASE = 'Wall_Back'
img_name = WALL_BACK_BASE + ".png"
json_name = WALL_BACK_BASE + ".json"
img_path = os.path.join(BASE_WALL_PATH, WALL_BACK_BASE, img_name)
json_path = os.path.join(BASE_WALL_PATH, WALL_BACK_BASE, json_name)
wall_back_sprite = Spritesheet(img_path, json_path)
wall_back = wall_back_sprite.get_frames()[0]
wall_left = wall_back.rotate_and_copy(90)
wall_right = wall_back.rotate_and_copy(-90)
TILE_IMAGE_ASSETS.append(wall_back)
TILE_IMAGE_ASSETS.append(wall_left)
TILE_IMAGE_ASSETS.append(wall_right)

WALL_BACK_CORNER_BASE = 'Wall_Corner'
img_name = WALL_BACK_CORNER_BASE + ".png"
json_name = WALL_BACK_CORNER_BASE + ".json"
img_path = os.path.join(BASE_WALL_PATH, WALL_BACK_CORNER_BASE, img_name)
json_path = os.path.join(BASE_WALL_PATH, WALL_BACK_CORNER_BASE, json_name)
wall_back_corner_sprite = Spritesheet(img_path, json_path)
wall_back_right_corner = wall_back_corner_sprite.get_frames()[0]
wall_back_left_corner = wall_back_right_corner.rotate_and_copy(90)
TILE_IMAGE_ASSETS.append(wall_back_right_corner)
TILE_IMAGE_ASSETS.append(wall_back_left_corner)

WALL_FRONT_LIST = ['Wall_Featured 1.0', 'Wall_Featured 1.1', 'Wall_Featured 2.0', 'Wall_Featured 3.0', 'Wall_Featured 3.1', 'Wall_Featured 4.0', 'Wall_Featured 5.0', 'Wall_Featured 6.0', 'Wall_Featured 7.0', 'Wall_Featured 8.0', 'Wall_Featured 9.0', 'Wall_Plain 1.0', 'Wall_Plain 1.1', 'Wall_Plain_Cracked 1', 'Wall_Plain_Cracked 2', 'Wall_Plain_Cracked 3', 'Wall_Solid']

for wall_front_name in WALL_FRONT_LIST:
    img_name = wall_front_name + ".png"
    json_name = wall_front_name + ".json"

    img_path = os.path.join(BASE_WALL_PATH, wall_front_name, img_name)
    json_path = os.path.join(BASE_WALL_PATH, wall_front_name, json_name)

    wall_front_sprite = Spritesheet(img_path, json_path)
    img = wall_front_sprite.get_frames()[0]
    img.resize(128, 128)
    TILE_IMAGE_ASSETS.append(img)

for tile_asset in TILE_IMAGE_ASSETS:
    tile_asset.resize(128, 128)