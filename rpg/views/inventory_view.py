"""
Inventory
"""
import arcade

import json

from arcade.gui import UIManager, UIAnchorWidget, UIBoxLayout, UIFlatButton, UITextureButton

from rpg.constants import SCREEN_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT, INVENTORY_WIDTH

def cargar_datos(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo {ruta_archivo} tiene formato JSON inválido")
        return None

ruta_player_json = "..\\resources\\data\\player_info.json"
ruta_items_json = "..\\resources\\data\\item_dictionary.json"
items = cargar_datos(ruta_items_json)
stats = cargar_datos(ruta_player_json)



class Item:
    def __init__(self, name, description, item_type):
        self.name = name
        self.description = description
        self.selected = False
        self.quantity = 1
        self.equipped = False
        self.item_type = item_type



class ItemButton(UIFlatButton):
    """Botón personalizado para los objetos del inventario"""

    def __init__(self, item, inventory_view, x=0, y=0, width=300, height=60, **kwargs):
        # Cambiar color si está seleccionado
        self.inventory_view = inventory_view  # Guardar referencia al InventoryView
        if item.equipped:
            bg_color = arcade.color.BLUE
        elif item.selected:
            bg_color = arcade.color.GOLD
        else:
            bg_color = arcade.color.LIGHT_GRAY
        super().__init__(
            text=f"{item.name}: {item.description} (x{item.quantity})",  # Mostrar cantidad
            x=x, y=y,
            width=width, height=height,
            style={
                "normal": {
                    "bg_color": bg_color,
                    "border_color": arcade.color.DARK_GRAY,
                    "font_color": arcade.color.BLACK
                },
                "hover": {
                    "bg_color": arcade.color.LIGHT_BLUE,
                    "border_color": arcade.color.DARK_GRAY,
                    "font_color": arcade.color.BLACK
                },
                "press": {
                    "bg_color": arcade.color.BLUEBERRY,
                    "border_color": arcade.color.DARK_GRAY,
                    "font_color": arcade.color.WHITE
                }
            },
            **kwargs
        )
        self.item = item

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.use_item()

    def on_click(self, event: arcade.gui.UIOnClickEvent):

        self.use_item()


    def use_item(self):
        """Ejemplo: usar una poción"""
        try:
            print(f"Usando {self.item.name}...")

            if self.item.name == "Potion":
                self.use_potion()
                self.item.quantity -= 1  # Solo disminuir cantidad si es consumible
                if self.item.quantity <= 0:
                    print("Intentando borrar item")
                    self.remove_item()
                else:
                    # Actualizar texto del botón con la nueva cantidad
                    self.text = f"{self.item.name}: {self.item.description} (x{self.item.quantity})"
                    # Recrear la UI para reflejar cambios
                    self.inventory_view.recreate_inventory_ui()
            elif self.item.name == "Sword":
                self.equip("Sword")
            else:
                print("Objeto no existe")
                return None
        except Exception as e:
            print(f"Error al usar el ítem: {e}")  # Debug




    def use_potion(self):
        """Ejemplo: usar una poción"""
        if stats["HP"] < (stats["HP_MAX"] - 50):
            stats["HP"] += 50
        else:
            stats["HP"] = stats["HP_MAX"]

        print("Usando poción... +50 HP")
        print(stats['HP'])

    def equip(self,item_name):

        if item_name == "Sword" and self.item.equipped == False:
          stats["EQUIPPED"] = items["Sword"]
          self.item.equipped = True
        else:
            print("Objeto ya equipado")

        print(stats["EQUIPPED"])

    def remove_item(self):
        """Elimina el objeto de la lista del jugador y actualiza la UI"""
        if self.item in self.inventory_view.player_items:
            self.inventory_view.player_items.remove(self.item)
            # Recrear la UI del inventario para reflejar los cambios
            self.inventory_view.recreate_inventory_ui()


class InventoryView(arcade.View) :
    def __init__(self):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)




        # Variables del juego
        self.player_items = []
        self.ui_manager = UIManager()

        # Crear algunos objetos de ejemplo
        self.setup_items()

        self.create_inventory_ui()

    def setup_items(self):
        # Crear objetos para el inventario (solo texto)
        item1 = Item("Sword", "Daño: 15","weapon")
        item2 = Item("Potion", "Cura 50 HP","potion")


        # Añadir múltiples instancias de algunos objetos
        item2.quantity = 3

        self.player_items.append(item1)
        self.player_items.append(item2)


    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Inventory",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width)

        # Dibujar objetos seleccionados en el HUD
        selected_items = [item for item in self.player_items if item.selected]
        for i, item in enumerate(selected_items):
            # Dibujar un recuadro con el nombre del objeto seleccionado
            arcade.draw_rectangle_filled(50 + i * 120, 50, 100, 40, arcade.color.GOLD)
            arcade.draw_text(item.name, 50 + i * 120, 50,
                             arcade.color.BLACK, 14,
                             align="center", anchor_x="center", anchor_y="center")

        # El UIManager se encarga de dibujar los botones del inventario
        self.ui_manager.draw()

    def recreate_inventory_ui(self):
        """Recrea la interfaz de usuario del inventario"""
        self.ui_manager.clear()  # Limpiar la UI actual
        self.create_inventory_ui()  # Volver a crear la UI
        
    def create_inventory_ui(self):
        # Panel principal del inventario
        panel = arcade.gui.UIBoxLayout(vertical=True, size_hint=(0.8, 0.8))

        # Lista de objetos
        item_list = arcade.gui.UIBoxLayout(vertical=True, size_hint=(1, 1))

        # Crear un botón para cada objeto
        for item in self.player_items:
            if item.quantity > 0:
                # Pasar self (InventoryView) como referencia al botón
                btn = ItemButton(item, self, width=INVENTORY_WIDTH - 40)
                item_list.add(btn.with_space_around(bottom=5))

        panel.add(item_list)

        # Añadir el inventario al centro de la pantalla
        self.ui_manager.add(UIAnchorWidget(
            anchor_x="center",
            anchor_y="center",
            child=panel
        ))





    def on_key_press(self, symbol: int, modifiers: int):
        closetomenu_inputs = [
            arcade.key.ESCAPE
        ]
        if symbol in closetomenu_inputs:
            self.window.show_view(self.window.views["main_menu"])

        closetogame_inputs = [
            arcade.key.I
        ]
        if symbol in closetogame_inputs:
            self.window.show_view(self.window.views["game"])

    def update(self, delta_time):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ALMOND)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

        self.ui_manager.enable()



    def on_hide_view(self):
        self.ui_manager.disable()