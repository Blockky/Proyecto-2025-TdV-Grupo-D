

import arcade

from resources.sounds.Sounds import footsteps_sound
from rpg import constants
from rpg.sprites.character_sprite import CharacterSprite
from rpg.views.settings_view import SettingsView


class PlayerSprite(CharacterSprite):
    def __init__(self, sheet_name):
        super().__init__(sheet_name)
        self.moving = False

        self.step_player = None #reproductor de los pasos

        self.flash_count = 0
        self.flashing = False

    # parpadea tras recibir daño
    def take_damage(self):
        if not self.flashing:
            self.flash_count = 0
            self.flashing = True
            arcade.schedule(self.flash_effect, 0.1)

    def flash_effect(self, delta_time):
        # alpha entre opaco y transparente
        self.alpha = 90 if self.alpha == 255 else 255
        self.flash_count += 1

        if self.flash_count >= constants.INMO_DELAY/0.1:  #numero de parpadeos
            self.alpha = 255
            arcade.unschedule(self.flash_effect)
            self.flashing = False


    def on_update(self, delta_time):
        super().on_update(delta_time)

        if self.moving:
            if self.step_player is None:
                self.step_player = arcade.play_sound(footsteps_sound, looping=True, volume = 0.35 * SettingsView.v_ef)
        else:
            if self.step_player is not None:
                arcade.stop_sound(self.step_player)
                self.step_player = None

        if self.change_x != 0 or self.change_y != 0:
            self.moving = True
        else:
            self.moving = False




