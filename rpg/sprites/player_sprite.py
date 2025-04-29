

import arcade

from resources.sounds.Sounds import footsteps_sound
from rpg.sprites.character_sprite import CharacterSprite
from rpg.views.settings_view import SettingsView


class PlayerSprite(CharacterSprite):
    def __init__(self, sheet_name):
        super().__init__(sheet_name)
        self.moving = False

        self.step_player = None

    def on_update(self, delta_time):
        super().on_update(delta_time)

        if self.moving:
            if self.step_player is None:
                self.step_player = arcade.play_sound(footsteps_sound, looping=True, volume = 0.35 * SettingsView.v_ef)
                print(0.35*SettingsView.v_ef)
        else:
            if self.step_player is not None:
                arcade.stop_sound(self.step_player)
                self.step_player = None

        if self.change_x != 0 or self.change_y != 0:
            self.moving = True
        else:
            self.moving = False




