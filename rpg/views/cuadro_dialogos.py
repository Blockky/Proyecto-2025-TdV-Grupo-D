import arcade

from rpg.constants import MESSAGE_BOX_FONT_SIZE, MESSAGE_BOX_MARGIN



class CuadroDialogos:

    def __init__(self):
        self.width = 500
        self.height = 50
        self.dialog_box_visible = False
        self.dialog_index = 0
        self.dialog_text = []

    def on_draw(self):

        if self.dialog_box_visible:
            arcade.draw_rectangle_filled(650, 150, 750, 200, arcade.color.PURPLE)

            # Obtener el texto actual y dividirlo
            texto_completo = self.dialog_text[self.dialog_index]
            lineas = self._dividir_texto(texto_completo, 70)  # 70 caracteres por línea

            # Dibujar cada línea
            for i, linea in enumerate(lineas):
                arcade.draw_text(linea, 300, 200 - (i * 25), arcade.color.WHITE, 14)

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



    def start_dialog(self, lines):
        self.dialog_text = lines
        self.dialog_index = 0
        self.dialog_box_visible = True

    def advance_dialog(self, combate):
        self.dialog_index += 1
        if self.dialog_index >= len(self.dialog_text):
            self.dialog_box_visible = False
            print("combate empieza")
            combate()
