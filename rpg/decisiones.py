import arcade
import arcade.gui




def decision(opciones, ataque, no_ataque, el_inventario):     # crea los tres botones para decidir que hacer durante un combate
    boton_box = arcade.gui.UIBoxLayout(vertical = False, space_between = 50)
    atacar = arcade.gui.UIFlatButton(text="Atacar", width=200)
    no_atacar = arcade.gui.UIFlatButton(text="No Atacar", width=200)
    inventario = arcade.gui.UIFlatButton(text="Inventario", width=200)

    widget_anclado = arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",align_y=-250,child=boton_box)

    def on_click_atacar(evento):        # al pulsar atacar ejecuta ataque
        print("a")
        ataque()
        opciones.remove(widget_anclado)


    def on_click_no_atacar(evento):     # al pulsar no atacar ejecuta no_ataque
        print("n")
        no_ataque()
        opciones.remove(widget_anclado)

    def on_click_inventario(evento):    #al pulsar inventario ejecuta el_inventario
        print("i")
        el_inventario()
        opciones.remove(widget_anclado)

    atacar.on_click = on_click_atacar
    no_atacar.on_click = on_click_no_atacar
    inventario.on_click = on_click_inventario

    boton_box.add(atacar.with_space_around(bottom=20))
    boton_box.add(no_atacar.with_space_around(bottom=20))
    boton_box.add(inventario.with_space_around(bottom=20))

    opciones.add(widget_anclado)
