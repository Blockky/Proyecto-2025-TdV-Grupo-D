"""
Python Arcade Community RPG

An open-source RPG
"""

import arcade

import json
from rpg.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH, DEFAULT_PLAYER_STATS
from rpg.views import LoadingView
from rpg.views.inventory_view import InventoryView
from rpg.views.shop_view import ShopView
from rpg.views import game_view


def reset_player_stats():
    """Restablece los stats del jugador a valores por defecto"""
    ruta_player_json = "..\\resources\\data\\player_info.json"
    try:
        with open(ruta_player_json, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_PLAYER_STATS, f, indent=4, ensure_ascii=False)
        print("Stats del jugador reseteados a valores por defecto")
    except Exception as e:
        print(f"Error al resetear stats: {e}")

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
        self.views = {}


        arcade.resources.add_resource_handle("characters", "../resources/characters")
        arcade.resources.add_resource_handle("maps", "../resources/maps")
        arcade.resources.add_resource_handle("data", "../resources/data")
        arcade.resources.add_resource_handle("sounds", "../resources/sounds")
        arcade.resources.add_resource_handle("misc", "../resources/misc")


def main():
    """Main method"""


    reset_player_stats()
    window = MyWindow()
    window.center_window()
    start_view = LoadingView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()



if __name__ == "__main__":
    main()
