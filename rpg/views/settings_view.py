"""
Settings
"""
import arcade
import arcade.gui
import rpg.constants as constants
from rpg.musica import reproduce_musica


class SettingsView(arcade.View):
    v_ef = 1
    v_music = 1.8
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.LILAC)
    #controlador de los botones y la agrupación de estos
        self.control = arcade.gui.UIManager()
        self.botones_caja = arcade.gui.UIBoxLayout(vertical = False, space_between = 50)
        self.botones_music = arcade.gui.UIBoxLayout(vertical = False, space_between = 50)
    # creo botones efectos de sonido
        #boton + de SF
        self.mas_sf = arcade.gui.UIFlatButton(text="+", width=70, height=40)
        self.mas_sf.on_click = self.pulso_mas_sf
        self.botones_caja.add(self.mas_sf)
        #boton - de SF
        self.menos_sf = arcade.gui.UIFlatButton(text="-", width=70, height=40)
        self.menos_sf.on_click = self.pulso_menos_sf
        self.botones_caja.add(self.menos_sf)
        #boton reset de SF
        self.reset = arcade.gui.UIFlatButton(text="Resetear", width=150, height=40)
        self.reset.on_click = self.pulso_reset
        self.botones_caja.add(self.reset)
    #creo botones musica
        # boton + de musica
        self.mas_music = arcade.gui.UIFlatButton(text="+", width=70, height=40)
        self.mas_music.on_click = self.pulso_mas_music
        self.botones_music.add(self.mas_music)
        # boton - de musica
        self.menos_music = arcade.gui.UIFlatButton(text="-", width=70, height=40)
        self.menos_music.on_click = self.pulso_menos_music
        self.botones_music.add(self.menos_music)
        # boton reset de musica
        self.reset_music = arcade.gui.UIFlatButton(text="Resetear", width=150, height=40)
        self.reset_music.on_click = self.pulso_reset_music
        self.botones_music.add(self.reset_music)
    #widgets anclados
        self.efectos_sonido = arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=150, align_x=-410, child=self.botones_caja)
        self.musica = arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=50, align_x=-410, child=self.botones_music)

    # añado los botones de efectos de sonido y de musica a sus controladores
        self.control.add(self.efectos_sonido)
        self.control.add(self.musica)




    def on_draw(self):
        arcade.start_render()
        self.control.draw()
        arcade.draw_text(
            "Settings",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.BLACK,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text("Volumen Efectos de Sonido: "+str(SettingsView.v_ef), 50, constants.SCREEN_HEIGHT - 170,arcade.color.BLACK,19)
        arcade.draw_text("Volumen de Música: " + str(SettingsView.v_music), 50, constants.SCREEN_HEIGHT - 280, arcade.color.BLACK, 19)
        arcade.draw_text("El volumen de la música solo se actualiza al cambiar de zona", 50, constants.SCREEN_HEIGHT - 360, arcade.color.BLACK, 10)

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.LILAC)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        self.control.enable() #controla los botones

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])

   #al pulsar reset
    def pulso_reset(self,event):
        SettingsView.v_ef = 1
   #al pulsar + de efectos de sonido
    def pulso_mas_sf(self,event):
        if SettingsView.v_ef < 2:
            SettingsView.v_ef += 0.1
            SettingsView.v_ef = round(SettingsView.v_ef, 1)
        if SettingsView.v_ef > 2:
            SettingsView.v_ef = 2
    # al pulsar - de efectos de sonido
    def pulso_menos_sf(self,event):
        if SettingsView.v_ef > 0:
            SettingsView.v_ef -= 0.1
            SettingsView.v_ef = round(SettingsView.v_ef, 1)
        if SettingsView.v_ef < 0:
            SettingsView.v_ef = 0


        # al pulsar reset musica
    def pulso_reset_music(self, event):
        from rpg.views.game_view import GameView

        SettingsView.v_music = 1.8
        reproduce_musica(GameView.get_curr_map_name())

        # al pulsar + de musica
    def pulso_mas_music(self, event):
        from rpg.views.game_view import GameView

        if SettingsView.v_music < 2:
            SettingsView.v_music += 0.1
            SettingsView.v_music = round(SettingsView.v_music, 1)
            reproduce_musica(GameView.get_curr_map_name())  # musica ambiente
        if SettingsView.v_music > 2:
            SettingsView.v_music = 2

        # al pulsar - de musica
    def pulso_menos_music(self, event):
        from rpg.views.game_view import GameView

        if SettingsView.v_music > 0:
            SettingsView.v_music -= 0.1
            SettingsView.v_music = round(SettingsView.v_music, 1)
            reproduce_musica(GameView.get_curr_map_name())
        if SettingsView.v_music < 0:
            SettingsView.v_music = 0

