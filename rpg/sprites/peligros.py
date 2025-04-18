import arcade



class Peligro(arcade.Sprite):     #Los peligros son sprites que te dañan al tocarlos

    def __init__(self, image_path, scale, center_x, center_y):
        super().__init__(image_path, scale)
        self.center_x = center_x
        self.center_y = center_y


class Proyectil(Peligro):      #Los proyectiles son peligros que desaparecen tras hacer daño
    objetivo = None
    impactado = False
    def __init__(self, image_path, scale, center_x, center_y, objetivo):
        super().__init__(image_path, scale,center_x, center_y)
        self.objetivo = objetivo

    def update(self):
        if self.impactado:              #Si choca con el jugador el proyectil desaparece
            self.remove_from_sprite_lists()

        if arcade.check_for_collision_with_list(self, self.objetivo):
            self.impactado = True