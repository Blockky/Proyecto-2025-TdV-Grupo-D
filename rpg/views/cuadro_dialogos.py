import arcade

from rpg.constants import MESSAGE_BOX_FONT_SIZE, MESSAGE_BOX_MARGIN
from dialogos import angel, angel2, angel3,gato, gato_comprar, gato_no_comprar, fantasma, fantasma2, fantasma3, aranna, aranna2, campana, campana2, campana_ayuda, robot, robot2, angel4, demonio, demonio2


class CuadroDialogos:
    def __init__(self, view, message):
        self.message = message
        self.view = view
        self.width = 500
        self.height = 50

    def on_draw(self):
        arcade.start_render()

        if self.dialog_box_visible:
            arcade.draw_rectangle_filled(400, 150, 750, 200, arcade.color.ORANGE)

            # Obtener el texto actual y dividirlo
            texto_completo = self.dialog_text[self.dialog_index]
            lineas = self._dividir_texto(texto_completo, 70)  # 70 caracteres por línea

            # Dibujar cada línea
            for i, linea in enumerate(lineas):
                arcade.draw_text(linea, 50, 200 - (i * 25), arcade.color.WHITE, 14)

    def _dividir_texto(self, texto, max_caracteres):
        """Divide el texto en líneas de máximo 'max_caracteres' caracteres"""
        palabras = texto.split(' ')
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            if len(linea_actual) + len(palabra) + 1 <= max_caracteres:
                linea_actual += ("" if not linea_actual else " ") + palabra
            else:
                lineas.append(linea_actual)
                linea_actual = palabra

        if linea_actual:
            lineas.append(linea_actual)

        return lineas

    def on_key_press(self, key, _modifiers):
        self.view.close_message_box()

        # Interacción con la H
        if key == arcade.key.H:
            if self.state == "exploration":
                hit = arcade.check_for_collision_with_list(self.player, self.npc_list)
                if hit:
                    self.start_dialog(angel)
                    self.state = "dialog"

        if key == arcade.key.SPACE:
            if self.state == "dialog":
                self.advance_dialog()


    def start_dialog(self, lines):
        self.dialog_text = lines
        self.dialog_index = 0
        self.dialog_box_visible = True
        self.state = "dialog"

    def advance_dialog(self):
        self.dialog_index += 1
        if self.dialog_index >= len(self.dialog_text):
            self.dialog_box_visible = False
            self.start_bullet_hell()