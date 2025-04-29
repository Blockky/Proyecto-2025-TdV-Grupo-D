"""
Settings
"""
import arcade
import arcade.gui
import rpg.constants as constants


class SettingsView(arcade.View):
    v_ef = 1
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)
    #controlador de los botones y la agrupación de estos
        self.control = arcade.gui.UIManager()
        self.botones_caja = arcade.gui.UIBoxLayout(vertical = False, space_between = 50)
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
    #widget anclado
        self.efectos_sonido = arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", align_y=150, align_x=-410, child=self.botones_caja)
    # añado los botones de efectos de sonido a su controlador
        self.control.add(self.efectos_sonido)




    def on_draw(self):
        arcade.start_render()
        self.control.draw()
        arcade.draw_text(
            "Settings",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        arcade.draw_text("Volumen Efectos de Sonido: "+str(SettingsView.v_ef), 50, 550,arcade.color.ALLOY_ORANGE,19)

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
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

