import arcade

from rpg.constants import MESSAGE_BOX_FONT_SIZE, MESSAGE_BOX_MARGIN


class MessageBox:
    def __init__(self, view, message):
        self.message = message
        self.view = view
        self.width = 500
        self.height = 150

    def on_draw(self):
        cx = self.view.window.width / 2
        cy = self.view.window.height / 2

        arcade.draw_rectangle_filled(
            cx,
            cy,
            self.width + MESSAGE_BOX_MARGIN * 2,
            self.height + MESSAGE_BOX_MARGIN * 2,
            arcade.color.LILAC,
        )
        arcade.draw_rectangle_outline(
            cx,
            cy,
            self.width + MESSAGE_BOX_MARGIN * 2,
            self.height + MESSAGE_BOX_MARGIN * 2,
            arcade.color.DEEP_LILAC,
            4,
        )

        arcade.draw_text(
            self.message,
            cx,
            cy,
            arcade.color.BLACK,
            MESSAGE_BOX_FONT_SIZE,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=500,
        )

    def on_key_press(self, _key, _modifiers):
        self.view.close_message_box()
