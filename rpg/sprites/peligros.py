import math

import arcade

from rpg import constants


class Peligro(arcade.Sprite):     #Los peligros son sprites que te dañan al tocarlos

    def __init__(self, texture=None, scale = 1, center_x = 0, center_y = 0):
        super().__init__(filename=None, scale=scale)

        if texture:
            self.texture = texture

            w, h = self.texture.width * self.scale, self.texture.height * self.scale
            self.set_hit_box([
                (-w / 8, -h / 6),
                (w / 8, -h / 6),
                (w / 8, h / 6),
                (-w / 8, h / 6)
            ])



        self.center_x = center_x
        self.center_y = center_y


class Proyectil(Peligro):      #Los proyectiles son peligros que desaparecen tras hacer daño

    def __init__(self, textura, scale, center_x, center_y, angle, speed, objetivo):
        super().__init__(texture=textura, scale=scale, center_x=center_x, center_y=center_y)

        self.objetivo = objetivo
        self.impactado = False

        radianes = math.radians(angle)
        self.change_x = math.cos(radianes) * speed
        self.change_y = math.sin(radianes) * speed

    def update(self):
        # Movimiento de los proyectiles
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Si choca con el jugador el proyectil desaparece
        if self.impactado:
            self.remove_from_sprite_lists()

        if arcade.check_for_collision(self, self.objetivo):
            self.impactado = True

        #Si un proyectil sale de la pantalla desaparece
        screen_margen = 150
        if self.center_x < -400 or self.center_x > constants.SCREEN_WIDTH + screen_margen or self.center_y < -screen_margen or self.center_y > constants.SCREEN_HEIGHT + screen_margen:
            self.remove_from_sprite_lists()