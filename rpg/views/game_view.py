"""
Main game view
"""

import json
from functools import partial
from typing import Callable

import arcade
import arcade.gui
import rpg.constants as constants
import rpg.bosses_spawn as bosses
from arcade.experimental.lights import Light
from pyglet.math import Vec2

from rpg import decisiones
from rpg.bosses_spawn import coloca_boses
from rpg.combate import CombatManager
from rpg.musica import reproduce_musica, musc_ambiente
from rpg.sprites.bosses_sprite import Boss, Slime, Fantasma
from rpg.views import inventory_view, shop_view, loading_view, dialogos

from resources.sounds.Sounds import damage_sound, combat_music, door_sound, ghost_sound, fantasma_combat_music
from rpg.constants import INMO_DELAY, DEFAULT_PLAYER_STATS
from rpg.decisiones import decision

from rpg.message_box import MessageBox
from rpg.sprites.peligros import Proyectil, Peligro

from rpg.sprites.player_sprite import PlayerSprite
from rpg.views.cuadro_dialogos import CuadroDialogos
from rpg.views.inventory_view import InventoryView
from rpg.views.main_menu_view import MainMenuView
from rpg.views.settings_view import SettingsView


def cargar_datos(ruta_archivo):
    with open(ruta_archivo) as f:
        return json.load(f)


ruta_player_json = "../resources/data/player_info.json"

stats = cargar_datos(ruta_player_json)

def reset_player_stats():
    """Restablece los stats del jugador a valores por defecto"""
    ruta_player_json = "..\\resources\\data\\player_info.json"
    try:
        with open(ruta_player_json, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_PLAYER_STATS, f, indent=4, ensure_ascii=False)
        print("Stats del jugador reseteados a valores por defecto")
    except Exception as e:
        print(f"Error al resetear stats: {e}")

class DebugMenu(arcade.gui.UIBorder, arcade.gui.UIWindowLikeMixin):
    def __init__(
        self,
        *,
        width: float,
        height: float,
        noclip_callback: Callable,
        hyper_callback: Callable,
    ):

        self.off_style = {
            "bg_color": arcade.color.BLACK,
        }

        self.on_style = {
            "bg_color": arcade.color.REDWOOD,
        }

        self.setup_noclip(noclip_callback)
        self.setup_hyper(hyper_callback)

        space = 10

        self._title = arcade.gui.UITextArea(
            text="DEBUG MENU",
            width=width - space,
            height=height - space,
            font_size=14,
            text_color=arcade.color.BLACK,
        )

        group = arcade.gui.UIPadding(
            bg_color=(255, 255, 255, 255),
            child=arcade.gui.UILayout(
                width=width,
                height=height,
                children=[
                    arcade.gui.UIAnchorWidget(
                        child=self._title,
                        anchor_x="left",
                        anchor_y="top",
                        align_x=10,
                        align_y=-10,
                    ),
                    arcade.gui.UIAnchorWidget(
                        child=arcade.gui.UIBoxLayout(
                            x=0,
                            y=0,
                            children=[
                                arcade.gui.UIPadding(
                                    child=self.noclip_button, pading=(5, 5, 5, 5)
                                ),
                                arcade.gui.UIPadding(
                                    child=self.hyper_button, padding=(5, 5, 5, 5)
                                ),
                            ],
                            vertical=False,
                        ),
                        anchor_x="left",
                        anchor_y="bottom",
                        align_x=5,
                    ),
                ],
            ),
        )

        # x and y don't seem to actually change where this is created. bug?
        # TODO: make this not appear at the complete bottom left (top left would be better?)
        super().__init__(border_width=5, child=group)

    def setup_noclip(self, callback: Callable):
        # disable player collision

        def toggle(*args):
            # toggle state on click
            self.noclip_status = True if not self.noclip_status else False
            self.noclip_button._style = (
                self.off_style if not self.noclip_status else self.on_style
            )
            self.noclip_button.clear()

            callback(status=self.noclip_status)

        self.noclip_status = False
        self.noclip_button = arcade.gui.UIFlatButton(
            text="noclip", style=self.off_style
        )
        self.noclip_button.on_click = toggle  # type: ignore

    def setup_hyper(self, callback: Callable):
        # increase player speed

        def toggle(*args):
            # toggle state on click
            self.hyper_status = True if not self.hyper_status else False
            self.hyper_button._style = (
                self.off_style if not self.hyper_status else self.on_style
            )
            self.hyper_button.clear()

            callback(status=self.hyper_status)

        self.hyper_status = False

        self.hyper_button = arcade.gui.UIFlatButton(text="hyper", style=self.off_style)
        self.hyper_button.on_click = toggle  # type: ignore


class GameView(arcade.View):
    """
    Main application class.
    """
    #el estado: está Exploration, Combat, Dialog y Locked
    state = "Exploration"

    #esto es para los dialogos en combate
    persuadiendo = False

    # Nombre del mapa en el que estamos
    curr_map_name = None #el mapa actual


    @classmethod
    def set_curr_map_name(cls, name): #para poder modificar el mapa actual comodamente
        cls.curr_map_name = name
    @classmethod
    def get_curr_map_name(cls):
        return cls.curr_map_name #para poder acceder al mapa actual comodamente


    def __init__(self, map_list, inventory_view, shop_view):
        super().__init__()
        self.inventory_view = inventory_view
        self.shop_view = shop_view

        reset_player_stats()
        self.reset_items()

        arcade.set_background_color(arcade.color.AMAZON)

        self.enemigo = None #para los bosses



        self.setup_debug_menu()


        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Player sprite
        self.player_sprite = None
        self.player_sprite_list = None

        #Vida

        self.hp = stats['HP']

        #Para hacer inmortal al personaje unos segundos
        self.inmortal = True
        self.timer = 0
        self.inmo_delay = INMO_DELAY

        #Lista de peligros
        self.peligro_sprite_list = arcade.SpriteList()

        # Gestiona los botones de la toma de decisiones
        self.opciones = arcade.gui.UIManager()
        self.opciones.enable()


        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Physics engine
        self.physics_engine = None

        # Maps
        self.map_list = map_list


        self.message_box = None

        # Selected Items Hotbar
        self.hotbar_sprite_list = None
        self.selected_item = 1

        f = open("../resources/data/item_dictionary.json")
        self.item_dictionary = json.load(f)

        f = open("../resources/data/characters_dictionary.json")
        self.enemy_dictionary = json.load(f)

        # Cameras
        self.camera_sprites = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)

        # Create a small white light
        x = 100
        y = 200
        radius = 150
        mode = "soft"
        color = arcade.csscolor.WHITE
        self.player_light = Light(x, y, radius, color, mode)

        #Crea el controlador de los dialogos
        self.dialog_manager = CuadroDialogos()

        # Crea los bosses
        self.angel = Boss("../resources/characters/Angel/Angel_Sprites.png",4,2,64,64, (400,1000), 3,1000,1000)
        self.angel2 = Boss("../resources/characters/Angel/Angel_Sprites.png", 4, 2, 64, 64, (200, 200), 2.5, 1000, 1000)
        self.angel3 = Boss("../resources/characters/Angel/Angel_Sprites.png", 4, 2, 64, 64, (190, 1000), 3, 1000, 1000)
        self.slime = Slime("../resources/characters/Slime/Slime_movbase.png","../resources/characters/Slime/Slime_Sprites.png",3,4,32,32, (170, 340), 3,50,3)
        self.fantasma = Fantasma("../resources/characters/Enemy/fantasma.png",3,4,32,32,(170,340),2.6,70,4)
    def reset_items(self):
        """Restablece los items del inventario a valores por defecto"""

        self.inventory_view.reset_items()
        print("Items del inventario reseteados")

    def reset_shop(self):
        """Restablece los items del inventario a valores por defecto"""

        self.shop_view.reset_shop()
        print("Items de la tienda reseteados")



    def switch_map(self, map_name, start_x, start_y):
        """
        Switch the current map
        :param map_name: Name of map to switch to
        :param start_x: Grid x location to spawn at
        :param start_y: Grid y location to spawn at
        """
        GameView.set_curr_map_name(map_name)

        try:
            self.my_map = self.map_list[GameView.get_curr_map_name()]
        except KeyError:
            raise KeyError(f"Unable to find map named '{map_name}'.")

        if self.my_map.background_color:
            arcade.set_background_color(self.my_map.background_color)

        map_height = self.my_map.map_size[1]
        self.player_sprite.center_x = (
            start_x * constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2
        )
        self.player_sprite.center_y = (
            map_height - start_y
        ) * constants.SPRITE_SIZE - constants.SPRITE_SIZE / 2
        self.scroll_to_player(1.0)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.setup_physics()

        if self.my_map.light_layer:
            self.my_map.light_layer.resize(self.window.width, self.window.height)

    def setup_physics(self):
        if self.noclip_status:
            # make an empty spritelist so the character does not collide with anyting
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, arcade.SpriteList()
            )
        else:
            # use the walls as normal
            self.physics_engine = arcade.PhysicsEngineSimple(
                self.player_sprite, self.my_map.scene["wall_list"]
            )


    def setup(self):
        """Set up the game variables. Call to re-start the game."""
        reset_player_stats()

        # Create the player character
        self.player_sprite = PlayerSprite(":characters:Male/main-character.png")

        # Spawn the player
        start_x = constants.STARTING_X
        start_y = constants.STARTING_Y
        self.switch_map(constants.STARTING_MAP, start_x, start_y)
        GameView.set_curr_map_name(constants.STARTING_MAP)
        # musica ambiente
        reproduce_musica(GameView.get_curr_map_name())

        #Establece el estado inicial
        GameView.state = "Exploration"
        #Se asegura de que los bosses spawneen bien
        self.colocar_los_bosses()
        #Revive al segundo angel para que aparezca donde el slime si mueres
        self.angel2.death = False

        # Set up the hotbar
        self.load_hotbar_sprites()

        # Establece la vida desde el JSON
        self.update_hp_from_json()




    def load_hotbar_sprites(self):
        """Load the sprites for the hotbar at the bottom of the screen.

        Loads the controls sprite tileset and selects only the number pad button sprites.
        These will be visual representations of number keypads (1️⃣, 2️⃣, 3️⃣, ..., 0️⃣)
        to clarify that the hotkey bar can be accessed through these keypresses.
        """

        first_number_pad_sprite_index = 51
        last_number_pad_sprite_index = 61

        self.hotbar_sprite_list = arcade.load_spritesheet(
            file_name="../resources/tilesets/input_prompts_kenney.png",
            sprite_width=16,
            sprite_height=16,
            columns=34,
            count=816,
            margin=1,
        )[first_number_pad_sprite_index:last_number_pad_sprite_index]

    def setup_debug_menu(self):
        self.debug = False

        self.debug_menu = DebugMenu(
            width=450,
            height=200,
            noclip_callback=self.noclip,
            hyper_callback=self.hyper,
        )

        self.original_movement_speed = constants.MOVEMENT_SPEED
        self.noclip_status = False

    def enable_debug_menu(self):
        self.ui_manager.add(self.debug_menu)

    def disable_debug_menu(self):
        self.ui_manager.remove(self.debug_menu)

    def noclip(self, *args, status: bool):
        self.noclip_status = status

        self.setup_physics()

    def hyper(self, *args, status: bool):
        constants.MOVEMENT_SPEED = (
            int(self.original_movement_speed * 3.5)
            if status
            else self.original_movement_speed
        )

    def draw_inventory(self):
        capacity = 10
        vertical_hotbar_location = 40
        hotbar_height = 80
        sprite_height = 16

    # Dibuja la interfaz
    def draw_interface(self):
        #Dibuja la vida
        for x in range (30, 30 + self.hp*50, 50):
            corazon = arcade.Sprite(r"../resources/misc/vida.png",0.35)
            corazon.center_x = x
            corazon.center_y = 690
            corazon.draw()



    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        cur_map = self.map_list[GameView.get_curr_map_name()]

        # --- Light related ---
        # Everything that should be affected by lights gets rendered inside this
        # 'with' statement. Nothing is rendered to the screen yet, just the light
        # layer.
        with cur_map.light_layer:
            arcade.set_background_color(cur_map.background_color)

            # Use the scrolling camera for sprites
            self.camera_sprites.use()

            # Grab each tile layer from the map
            map_layers = cur_map.map_layers

            # Draw scene
            cur_map.scene.draw()

            for item in map_layers.get("searchable", []):
                arcade.Sprite(
                    filename=":misc:shiny-stars.png",
                    center_x=item.center_x,
                    center_y=item.center_y,
                    scale=0.8,
                ).draw()

            # Draw the player
            self.player_sprite_list.draw()

            # Dibuja los objetos dañinos
            self.peligro_sprite_list.draw()

        if cur_map.light_layer:
            # Draw the light layer to the screen.
            # This fills the entire screen with the lit version
            # of what we drew into the light layer above.
            if cur_map.properties and "ambient_color" in cur_map.properties:
                ambient_color = cur_map.properties["ambient_color"]
                # ambient_color = (ambient_color.green, ambient_color.blue, ambient_color.alpha, ambient_color.red)
            else:
                ambient_color = arcade.color.WHITE
            cur_map.light_layer.draw(ambient_color=ambient_color)

        # Use the non-scrolled GUI camera
        self.camera_gui.use()


        #Dibuja la vida en pantalla
        self.draw_interface()

        #Dibuja los botones de la decision en combate cuando sean necesarios
        self.opciones.draw()

        # Draw any message boxes
        if self.message_box:
            self.message_box.on_draw()

        #Dibuja los dialogos:
        self.dialog_manager.on_draw()

        # draw GUI
        self.ui_manager.draw()

    def scroll_to_player(self, speed=constants.CAMERA_SPEED):
        """Manage Scrolling"""

        vector = Vec2(
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2,
        )
        self.camera_sprites.move_to(vector, speed)

    def on_show_view(self):
        # Set background color
        my_map = self.map_list[GameView.get_curr_map_name()]
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)


        # Actualizar HP desde el JSON al mostrar la vista
        self.update_hp_from_json()

    def update_hp_from_json(self):
        """Actualiza self.hp con el valor actual del JSON"""
        global stats
        try:
            # Cargar datos actualizados
            stats = cargar_datos(ruta_player_json)
            self.hp = stats['HP']
            print(f"Vida actualizada: {self.hp}/{stats['HP_MAX']}")
        except Exception as e:
            print(f"Error al actualizar HP desde JSON: {e}")


    # Sistema de perder vida con peligros y proyectiles
    def peligros(self):
        for peligro in self.peligro_sprite_list:
            if self.inmortal == False:
                hit_list = arcade.check_for_collision_with_list(peligro, self.player_sprite_list)
            else:
                hit_list = []

            # Si golpeó: el jugador pierde una vida y se hace temporalmente inmortal
            if len(hit_list) > 0:
                self.hp -= 1
                stats['HP'] = self.hp  # Actualizar el diccionario global

                # Guardar el cambio en el JSON
                try:
                    with open(ruta_player_json, 'w', encoding='utf-8') as f:
                        json.dump(stats, f, indent=4, ensure_ascii=False)
                except Exception as e:
                    print(f"Error al guardar daño en JSON: {e}")

                arcade.play_sound(damage_sound, volume=0.4 * SettingsView.v_ef)
                self.player_sprite.take_damage()
                self.inmortal = True

    #para colocar los bosses en sus salas
    def colocar_los_bosses(self):
        coloca_boses(GameView.get_curr_map_name(), self.peligro_sprite_list, self.angel, self.slime, self.angel2, self.angel3, self.fantasma)

    def start_combat(self,boss):
        self.combat_manager = CombatManager(self.player_sprite, boss, self.peligro_sprite_list,GameView.get_curr_map_name(), self.opciones,lambda: self.colocar_los_bosses(), self.dialog_manager, lambda: self.window.show_view(self.window.views["inventory"]))

        # si es el primer combate contra el slime, el angel debe desaparecer tras hablarte
        if boss == self.slime:
            self.angel2.death = True
            self.colocar_los_bosses()

        GameView.state = "Combat"
        if GameView.get_curr_map_name() == "mapa_boss_fantasma":
            musc_ambiente(fantasma_combat_music, 0.15)
        else:
            musc_ambiente(combat_music, 0.7)

    def dialog_start(self, boss_dialog): #comienza dialogo, usar esto casi siempre
        self.dialog_manager.start_dialog(boss_dialog)
        GameView.state = "Dialog"

    def angel_dialog(self): # parece inutil pero es necesario para dialogos con el angel
        GameView.state = "Exploration"
        self.angel.death = True

    def angel3_dialog(self): # esto es muy sucio pero es lo mejor que se me ha ocurrido
        GameView.state = "Exploration"
        self.angel3.death = True

    def angel_slime_combat_dialog(self): #también es necesario
        decisiones.tutorial = False

    def combat_dialog(self):
        GameView.persuadiendo = False
        self.combat_manager.persuadir()

    def exploration_dialog(self): # esto es muy sucio pero es lo mejor que se me ha ocurrido
        GameView.state = "Exploration"



    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        MOVING_UP = (
            self.up_pressed
            and not self.down_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        MOVING_DOWN = (
            self.down_pressed
            and not self.up_pressed
            and not self.right_pressed
            and not self.left_pressed
        )

        MOVING_RIGHT = (
            self.right_pressed
            and not self.left_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        MOVING_LEFT = (
            self.left_pressed
            and not self.right_pressed
            and not self.up_pressed
            and not self.down_pressed
        )

        MOVING_UP_LEFT = (
            self.up_pressed
            and self.left_pressed
            and not self.down_pressed
            and not self.right_pressed
        )

        MOVING_DOWN_LEFT = (
            self.down_pressed
            and self.left_pressed
            and not self.up_pressed
            and not self.right_pressed
        )

        MOVING_UP_RIGHT = (
            self.up_pressed
            and self.right_pressed
            and not self.down_pressed
            and not self.left_pressed
        )

        MOVING_DOWN_RIGHT = (
            self.down_pressed
            and self.right_pressed
            and not self.up_pressed
            and not self.left_pressed
        )

        if MOVING_UP:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED

        if MOVING_DOWN:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED

        if MOVING_LEFT:
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED

        if MOVING_RIGHT:
            self.player_sprite.change_x = constants.MOVEMENT_SPEED

        if MOVING_UP_LEFT:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if MOVING_UP_RIGHT:
            self.player_sprite.change_y = constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        if MOVING_DOWN_LEFT:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = -constants.MOVEMENT_SPEED / 1.5

        if MOVING_DOWN_RIGHT:
            self.player_sprite.change_y = -constants.MOVEMENT_SPEED / 1.5
            self.player_sprite.change_x = constants.MOVEMENT_SPEED / 1.5

        # Call update to move the sprite
        self.physics_engine.update()

        # Update player animation
        self.player_sprite_list.on_update(delta_time)

        self.player_light.position = self.player_sprite.position

        #Update de los Proyectiles
        self.peligro_sprite_list.update()

        # Update the characters
        try:
            self.map_list[GameView.get_curr_map_name()].scene["characters"].on_update(delta_time)
        except KeyError:
            # no characters on map
            pass

        # --- Manage doors ---
        map_layers = self.map_list[GameView.get_curr_map_name()].map_layers

        # Is there as layer named 'doors'?
        if "doors" in map_layers:
            # Did we hit a door?
            doors_hit = arcade.check_for_collision_with_list(
                self.player_sprite, map_layers["doors"]
            )
            # We did!
            if len(doors_hit) > 0:
                try:
                    # Grab the info we need
                    map_name = doors_hit[0].properties["map_name"]
                    start_x = doors_hit[0].properties["start_x"]
                    start_y = doors_hit[0].properties["start_y"]
                except KeyError:
                    raise KeyError(
                        "Door objects must have 'map_name', 'start_x', and 'start_y' properties defined."
                    )

                # Swap to the new map
                if GameView.state == "Exploration" or GameView.state == "Locked":
                    if GameView.state == "Locked" and (GameView.get_curr_map_name() == "mapa_boss_slime" or GameView.get_curr_map_name() == "mapa_boss_angel" or GameView.get_curr_map_name() == "mapa_boss_arana" or GameView.get_curr_map_name() == "mapa_boss_campana" or GameView.get_curr_map_name() == "mapa_boss_fantasma" or GameView.get_curr_map_name() == "mapa_boss_robot"or GameView.get_curr_map_name() == "StartingRoomMap" ):
                        pass
                    else:
                        self.switch_map(map_name, start_x, start_y)
                        arcade.play_sound(door_sound, volume=0.35 * SettingsView.v_ef)

                    # Determina que musica reproducir
                    reproduce_musica(GameView.get_curr_map_name())
                    # Aparece es boss, si es necesario
                    self.colocar_los_bosses()

            else:
                # We didn't hit a door, scroll normally
                self.scroll_to_player()
        else:
            # No doors, scroll normally
            self.scroll_to_player()

        #Reproduce la animación de los bosses
        self.peligro_sprite_list.update_animation(delta_time)

        #Ejecuta que los peligros funcionen
        self.peligros()
        #Te hace inmortal unos segundos tras recibir daño
        if self.inmortal and GameView.state == "Combat":
            self.timer += delta_time
            if self.timer >= self.inmo_delay:
                self.inmortal = False
                self.timer = 0
        elif not self.inmortal and GameView.state != "Combat":
            self.inmortal = True

        #Si la vida llega a 0 mueres
        if self.hp <= 0:
            print("Moriste")
            # Resetear vida en el JSON
            stats['HP'] = DEFAULT_PLAYER_STATS['HP']
            try:
                with open(ruta_player_json, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Error al resetear vida: {e}")
            # Resetear el inventario
            self.reset_items()
            # Resetear la tienda
            self.reset_shop()

            # Reiniciar el juego
            self.window.views["game"].setup()
            self.window.show_view(self.window.views["game"])


        #si estamos en combate, se actualiza el combate
        if GameView.state == "Combat":
            self.combat_manager.update(delta_time)

        #En dialogo no se puede andar
        if GameView.state == "Dialog":
            if self.up_pressed or self.down_pressed or self.left_pressed or self.right_pressed:
                self.up_pressed = False
                self.down_pressed = False
                self.left_pressed = False
                self.right_pressed = False


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if self.message_box:
            self.message_box.on_key_press(key, modifiers)
            return
        if GameView.state != "Dialog":  #no se puede mover en dialogo
            if key in constants.KEY_UP:
                self.up_pressed = True
            elif key in constants.KEY_DOWN:
                self.down_pressed = True
            elif key in constants.KEY_LEFT:
                self.left_pressed = True
            elif key in constants.KEY_RIGHT:
                self.right_pressed = True
        if key in constants.INVENTORY:
            if GameView.state == "Exploration" or GameView.state == "Locked":
                self.window.show_view(self.window.views["inventory"])
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])
        elif key in constants.SEARCH:
            self.search()
        elif key == arcade.key.KEY_1:
            stats['HP']= 0
            # Guardar los cambios en el archivo JSON
            try:
                with open(ruta_player_json, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, indent=4, ensure_ascii=False)
                print("Datos del jugador actualizados correctamente.")
            except Exception as e:
                print(f"Error al guardar los datos: {e}")
            self.hp = 0
        elif key == arcade.key.KEY_2:
            self.selected_item = 2
        elif key == arcade.key.KEY_3:
            self.selected_item = 3
        elif key == arcade.key.KEY_4:
            self.selected_item = 4
        elif key == arcade.key.KEY_5:
            self.selected_item = 5
        elif key == arcade.key.KEY_6:
            self.selected_item = 6
        elif key == arcade.key.KEY_7:
            self.selected_item = 7
        elif key == arcade.key.KEY_8:
            self.selected_item = 8
        elif key == arcade.key.KEY_9:
            self.selected_item = 9
        elif key == arcade.key.KEY_0:
            self.selected_item = 10
        elif key == arcade.key.L: #linterna (la he desactivado)
            #cur_map = self.map_list[GameView.get_curr_map_name()]
            #if self.player_light in cur_map.light_layer:
                #cur_map.light_layer.remove(self.player_light)
            #else:
                #cur_map.light_layer.add(self.player_light)
            pass
        elif key == arcade.key.G:  # G
            # toggle debug
            self.debug = True if not self.debug else False
            if self.debug:
                self.enable_debug_menu()
            else:
                self.disable_debug_menu()

        #interactuar con npc
        if key == arcade.key.E:
            if GameView.state == "Exploration": #dialogos en bucle
                hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.peligro_sprite_list)
                if self.angel in hit_list:
                    self.dialog_start(dialogos.angel_loop)
                elif self.angel3 in hit_list:
                    self.dialog_start(dialogos.angel3_loop)
                elif self.fantasma in hit_list:
                    self.dialog_start(dialogos.fantasma3)
            elif GameView.state == "Locked":
                hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.peligro_sprite_list)
                #Hablar con el angel
                if self.angel2 in hit_list:
                    self.dialog_start(dialogos.angel2)
                elif self.angel in hit_list:
                    self.dialog_start(dialogos.angel)
                elif self.angel3 in hit_list:
                        self.dialog_start(dialogos.angel3)
                #Hablar con el fantasma
                if self.fantasma in hit_list:
                    if self.fantasma.convencido >= self.fantasma.boss_anger:
                        self.dialog_start(dialogos.fantasma2)
                    else:
                        self.dialog_start(dialogos.fantasma)
                    arcade.play_sound(ghost_sound, volume=0.4 * SettingsView.v_ef)


        #pasar entre dialogos
        if key == arcade.key.SPACE:
            if GameView.state == "Dialog":
                if GameView.get_curr_map_name() == "StartingRoomMap":
                    self.dialog_manager.advance_dialog(lambda: self.angel_dialog())
                elif GameView.get_curr_map_name() == "mapa_boss_slime":
                    if self.angel2.death:
                        if GameView.persuadiendo:
                            self.dialog_manager.advance_dialog(lambda: self.combat_dialog())
                        else:
                            self.dialog_manager.advance_dialog(lambda: self.angel_slime_combat_dialog())

                    else:
                        self.dialog_manager.advance_dialog(lambda: self.start_combat(self.slime))
                elif GameView.get_curr_map_name() == "salaExp_S1":
                    self.dialog_manager.advance_dialog(lambda: self.angel3_dialog())
                elif self.fantasma.convencido >= self.fantasma.boss_anger:
                    self.dialog_manager.advance_dialog(lambda: self.exploration_dialog())
                else:
                    if GameView.persuadiendo:
                        self.dialog_manager.advance_dialog(lambda: self.combat_dialog())
                    else:
                        self.dialog_manager.advance_dialog(lambda: self.start_combat(self.fantasma))





    def close_message_box(self):
        self.message_box = None

    def search(self):
        """Search for things"""
        map_layers = self.map_list[GameView.get_curr_map_name()].map_layers
        if "searchable" not in map_layers:
            print(f"No searchable sprites on {GameView.get_curr_map_name()} map layer.")
            return

        searchable_sprites = map_layers["searchable"]
        sprites_in_range = arcade.check_for_collision_with_list(
            self.player_sprite, searchable_sprites
        )
        print(f"Found {len(sprites_in_range)} searchable sprite(s) in range.")
        for sprite in sprites_in_range:
            if "item" in sprite.properties:
                self.message_box = MessageBox(
                    self, f"Found: {sprite.properties['item']}"
                )
                sprite.remove_from_sprite_lists()
                lookup_item = self.item_dictionary[sprite.properties["item"]]
                self.player_sprite.inventory.append(lookup_item)
            else:
                print(
                    "The 'item' property was not set for the sprite. Can't get any items from this."
                )

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key in constants.KEY_UP:
            self.up_pressed = False
        elif key in constants.KEY_DOWN:
            self.down_pressed = False
        elif key in constants.KEY_LEFT:
            self.left_pressed = False
        elif key in constants.KEY_RIGHT:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves."""
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """Called when the user presses a mouse button."""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player_sprite.destination_point = x, y

    def on_mouse_release(self, x, y, button, key_modifiers):
        """Called when a user releases a mouse button."""
        pass

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(width, height)
        self.camera_gui.resize(width, height)
        cur_map = self.map_list[GameView.get_curr_map_name()]
        if cur_map.light_layer:
            cur_map.light_layer.resize(width, height)
