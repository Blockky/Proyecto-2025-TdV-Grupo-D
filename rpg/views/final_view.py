"""
Final screen
"""
import arcade

class FinalView(arcade.View):
    def __init__(self):
        super().__init__()
        self.map_list = None
        arcade.set_background_color(arcade.color.LILAC)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "FIN DEL JUEGO",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.BLACK,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def setup(self):
        pass

    def update(self, delta_time: float):
        if