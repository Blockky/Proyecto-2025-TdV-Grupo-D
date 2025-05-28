import arcade
import arcade.gui

from rpg.views import dialogos


dialogos_tutorial = 0
tutorial = False
def decision(opciones, ataque, no_ataque, el_inventario, dialog_manager):     # crea los tres botones para decidir que hacer durante un combate
    from rpg.views.game_view import GameView


    boton_box = arcade.gui.UIBoxLayout(vertical = False, space_between = 50)
    atacar = arcade.gui.UIFlatButton(text="Atacar", width=200)
    no_atacar = arcade.gui.UIFlatButton(text="Dialogar", width=200)
    inventario = arcade.gui.UIFlatButton(text="Inventario", width=200)
    global dialogos_tutorial
    global tutorial


    #dialogos del combate tutorial
    if GameView.get_curr_map_name() == "mapa_boss_slime":
        dialogos_tutorial += 1
        if dialogos_tutorial == 1:
            dialog_manager.start_dialog(dialogos.angel_slime1)
            tutorial = True
        if dialogos_tutorial == 2:
            dialog_manager.start_dialog(dialogos.angel_slime2)
            tutorial = True
        if dialogos_tutorial >= 3:
            dialog_manager.start_dialog(dialogos.angel_slime3)
            tutorial = True

    widget_anclado = arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",align_y=-250,child=boton_box)


    def on_click_atacar(evento):        # al pulsar atacar ejecuta ataque
        if not tutorial:
            ataque()
            opciones.remove(widget_anclado)


    def on_click_no_atacar(evento):     # al pulsar no atacar ejecuta no_ataque
        if not tutorial:
            dialog_manager.start_dialog(dialogos.angel_slime_dialogar)
            GameView.persuadiendo = True
            opciones.remove(widget_anclado)

    def on_click_inventario(evento):    #al pulsar inventario ejecuta el_inventario
        if not tutorial:
            el_inventario()
            opciones.remove(widget_anclado)





    atacar.on_click = on_click_atacar
    no_atacar.on_click = on_click_no_atacar
    inventario.on_click = on_click_inventario

    boton_box.add(atacar.with_space_around(bottom=20))
    boton_box.add(no_atacar.with_space_around(bottom=20))
    boton_box.add(inventario.with_space_around(bottom=20))

    opciones.add(widget_anclado)
