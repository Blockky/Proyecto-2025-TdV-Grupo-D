"""
Shop
"""
import arcade

import json

from arcade.gui import UIManager, UIAnchorWidget, UIBoxLayout, UIFlatButton, UITextureButton

from rpg.constants import SCREEN_HEIGHT, SCREEN_WIDTH, INVENTORY_HEIGHT, INVENTORY_WIDTH

from rpg.views import inventory_view




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
    def __init__(self, name, description, item_type, buy_value):
        self.name = name
        self.description = description
        self.selected = False
        self.quantity = 1
        self.equipped = False
        self.item_type = item_type
        self.buy_value = buy_value


class ItemButton(UIFlatButton):
    """Botón personalizado para los objetos del inventario"""

    def __init__(self, item, shop_view, x=0, y=0, width=300, height=60, **kwargs):
        # Cambiar color si está seleccionado
        self.shop_view = shop_view  # Guardar referencia al ShopView
        if item.equipped:
            bg_color = arcade.color.BLUE
        elif item.selected:
            bg_color = arcade.color.GOLD
        else:
            bg_color = arcade.color.LIGHT_GRAY
        super().__init__(
            text=f"{item.name}: {item.description} (x{item.quantity}) ({item.buy_value} $)",  # Mostrar cantidad
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
        # Diálogo de confirmación
        confirm_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=f"¿Comprar {self.item.name} por {self.item.buy_value}?",
            buttons=["Sí", "No"],
            callback=self.on_confirmation_response
        )

        self.shop_view.ui_manager.add(confirm_box)


    def on_confirmation_response(self, response):
        if response == "Sí":
            success = self.shop_view.process_purchase(self.item)

            # Diálogo de resultado
            if success:
                message = f"¡Comprado {self.item.name}!"
            else:
                message = "No tienes suficiente dinero"

            result_box = arcade.gui.UIMessageBox(
                width=300,
                height=200,
                message_text=message,
                buttons=["OK"]
            )
            self.shop_view.ui_manager.add(result_box)


class ShopView(arcade.View):
    def __init__(self, inventory_view):
        super().__init__()
        self.started = False
        arcade.set_background_color(arcade.color.ALMOND)

        # Variables de la tienda
        self.shop_items = []
        self.ui_manager = UIManager()
        self.inventory_view = inventory_view

        # Crear algunos objetos de ejemplo
        self.setup_items()

        self.create_shop_ui()


    def setup_items(self):
        # Crear objetos para el inventario (solo texto)
        item1 = Item("Sword", "Daño: 15","weapon",15)
        item2 = Item("Potion", "Cura 50 HP","potion",15)


        # Añadir múltiples instancias de algunos objetos
        item2.quantity = 3

        self.shop_items.append(item1)
        self.shop_items.append(item2)

    def process_purchase(self, item):
        """Intenta realizar la compra y devuelve True/False si tuvo éxito"""
        if stats['GOLD'] >= item.buy_value:
            stats['GOLD'] -= item.buy_value
            self.gold_text = f"Gold: {stats['GOLD']}"

            # Convertir el ShopItem a InventoryItem (excluyendo buy_value)
            new_item = inventory_view.Item(
                name=item.name,
                description=item.description,
                item_type=item.item_type
            )
            new_item.quantity = 1  # Siempre compras 1 unidad

            # Añadir el nuevo objeto al inventario
            self.add_item(new_item)

            # Reducir la cantidad en la tienda
            item.quantity -= 1
            if item.quantity <= 0:
                self.shop_items.remove(item)

            print("¡Item comprado y añadido al inventario!")
            self.recreate_shop_ui()
            return True

        print("No tienes suficiente dinero")
        return False

    def add_item(self, item):
        """Añade el ítem comprado al inventario del jugador"""
        # Crea un nuevo Item (sin buy_value, ya que no es necesario en el inventario)
        new_item = inventory_view.Item(
            name=item.name,
            description=item.description,
            item_type=item.item_type
        )
        # Llama al metodo add_item de InventoryView
        self.inventory_view.add_item(new_item)




    def on_draw(self):
        arcade.start_render()

        self.gold_text = f"Gold: {stats['GOLD']}"

        arcade.draw_text(
            "The Shop",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width)

        arcade.draw_text(
            self.gold_text,
            self.window.width / 2,
            self.window.height - 600,
            arcade.color.GOLD,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

        # Dibujar objetos seleccionados en el HUD
        selected_items = [item for item in self.shop_items if item.selected]
        for i, item in enumerate(selected_items):
            # Dibujar un recuadro con el nombre del objeto seleccionado
            arcade.draw_rectangle_filled(50 + i * 120, 50, 100, 40, arcade.color.GOLD)
            arcade.draw_text(item.name, 50 + i * 120, 50,
                             arcade.color.BLACK, 14,
                             align="center", anchor_x="center", anchor_y="center")

        # El UIManager se encarga de dibujar los botones del inventario
        self.ui_manager.draw()

    def recreate_shop_ui(self):
        """Recrea la interfaz de usuario del inventario"""
        self.ui_manager.clear()  # Limpiar la UI actual
        self.create_shop_ui()  # Volver a crear la UI

    def create_shop_ui(self):
        # Panel principal del inventario
        panel = arcade.gui.UIBoxLayout(vertical=True, size_hint=(0.8, 0.8))

        # Lista de objetos
        item_list = arcade.gui.UIBoxLayout(vertical=True, size_hint=(1, 1))

        # Crear un botón para cada objeto
        for item in self.shop_items:
            if item.quantity > 0:
                # Pasar self (InventoryView) como referencia al botón
                btn = ItemButton(item, self, width=INVENTORY_WIDTH - 600)
                item_list.add(btn.with_space_around(bottom=5))

        panel.add(item_list)

        # Añadir el inventario al centro de la pantalla
        self.ui_manager.add(UIAnchorWidget(
            anchor_x="center",
            anchor_y="center",
            child=panel
        ))


    def setup(self):
        pass


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


