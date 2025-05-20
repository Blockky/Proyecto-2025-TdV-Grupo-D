"""
Constant values for the game
"""
import arcade
from arcade.examples.astar_pathfinding import MOVEMENT_SPEED
import json

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Python Community RPG"
TILE_SCALING = 1.2
SPRITE_SIZE = 32

INVENTORY_WIDTH = 1280
INVENTORY_HEIGHT = 720

# How fast does the player move
MOVEMENT_SPEED = 3

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 300

# What map, and what position we start at
STARTING_MAP = "salaExp_I"
STARTING_X = 4
STARTING_Y = 14

# Key mappings
KEY_UP = [arcade.key.UP, arcade.key.W]
KEY_DOWN = [arcade.key.DOWN, arcade.key.S]
KEY_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_RIGHT = [arcade.key.RIGHT, arcade.key.D]
INVENTORY = [arcade.key.I]
SEARCH = [arcade.key.E]

# Message box
MESSAGE_BOX_FONT_SIZE = 38
MESSAGE_BOX_MARGIN = 30

# How fast does the camera pan to the user
CAMERA_SPEED = 0.8


def cargar_datos(ruta_archivo):
    with open(ruta_archivo) as f:
        return json.load(f)


ruta_player_json = "../resources/data/player_info.json"

stats = cargar_datos(ruta_player_json)

# STATS INICIALES (AQUELLOS CUANDO SE INICIA EL JUEGO O MUERES)

DEFAULT_PLAYER_STATS = {
    "HP": 5,
    "HP_MAX": 10,
    "ATK": 5,
    "GOLD": 50,
    "EQUIPPED": {
        "short_name": "None",
        "type": "weapon",
        "damage_amount": 0
    }
}

#Segundos de invulnerabilidad tras recibir un golpe
INMO_DELAY = 2
