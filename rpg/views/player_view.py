
"""
Settings
"""
import arcade
import rpg.constants as constants
import json
import os

def cargar_datos(ruta_archivo):
        with open(ruta_archivo) as f:
            return json.load(f)


ruta_player_json = "..\\resources\\data\\player_info.json"

stats = cargar_datos(ruta_player_json)

class PlayerView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.GRAY)



        self.hp_text = f"HP: {stats['HP']}/{stats['HP_MAX']}"
        self.atk_text = f"ATK: {stats['ATK']}"
        self.gold_text = f"Gold: {stats['GOLD']}"
        if stats['EQUIPPED'] == "None":
            self.equipped_text = f"Weapon equipped: {stats['EQUIPPED']} (+0ATK)"




    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Player Stats",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",


        )
        arcade.draw_text(
            self.hp_text,
            self.window.width / 2,
            self.window.height - 200,
            arcade.color.GREEN,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            self.atk_text,
            self.window.width / 2,
            self.window.height - 300,
            arcade.color.RED,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            self.gold_text,
            self.window.width / 2,
            self.window.height - 400,
            arcade.color.GOLD,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text(
            self.equipped_text,
            self.window.width / 2,
            self.window.height - 600,
            arcade.color.BLUE_SAPPHIRE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GRAY)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])