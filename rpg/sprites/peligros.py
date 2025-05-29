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
        screen_margen = 200
        if self.center_x < -400 or self.center_x > constants.SCREEN_WIDTH + screen_margen or self.center_y < -screen_margen-55 or self.center_y > constants.SCREEN_HEIGHT + screen_margen:
            self.remove_from_sprite_lists()

class Esbirro(Proyectil):
    def __init__(self, texture_path, scale, center_x, center_y, angle, speed, objetivo, perseguir_jugador=False):
        self.direccional_textures = {
            "abajo": [],
            "izquierda": [],
            "derecha": [],
            "arriba": []
        }

        frame_width = 32
        frame_height = 32
        fila_direcciones = ["abajo", "izquierda", "derecha", "arriba"]

        for fila in range(4):
            for columna in range(3):
                frame = arcade.load_texture(
                    texture_path,
                    x=columna * frame_width,
                    y=fila * frame_height,
                    width=frame_width,
                    height=frame_height
                )
                self.direccional_textures[fila_direcciones[fila]].append(frame)

        # Usa el primer frame de 'abajo' como textura inicial
        super().__init__(self.direccional_textures["abajo"][0], scale, center_x, center_y, angle, speed, objetivo)

        self.perseguir_jugador = perseguir_jugador
        self.frame_actual = 0
        self.tiempo_animacion = 0
        self.tiempo_por_frame = 0.2

    def update(self, delta_time=1/60):
        # Persecución al jugador solo si está lejos
        if self.perseguir_jugador:
            dx = self.objetivo.center_x - self.center_x
            dy = self.objetivo.center_y - self.center_y
            distancia = math.hypot(dx, dy)

            distancia_minima = 50  # distancia mínima para dejar de perseguir

            if distancia > distancia_minima:
                angulo = math.atan2(dy, dx)
                velocidad = math.hypot(self.change_x, self.change_y)
                self.change_x = math.cos(angulo) * velocidad
                self.change_y = math.sin(angulo) * velocidad
            else:
                # Deja de moverse cuando está cerca
                self.perseguir_jugador = False

        # la lógica de movimiento y colisión de su clase padre
        super().update()

        # Animación del sprite
        self.tiempo_animacion += delta_time
        if self.tiempo_animacion >= self.tiempo_por_frame:
            self.frame_actual = (self.frame_actual + 1) % 3
            self.tiempo_animacion = 0

            # Determina la dirección actual
            if abs(self.change_x) > abs(self.change_y):
                direccion = "derecha" if self.change_x > 0 else "izquierda"
            else:
                direccion = "arriba" if self.change_y > 0 else "abajo"

            self.texture = self.direccional_textures[direccion][self.frame_actual]

class Rayo(Proyectil):
    def __init__(self, textura, scale, center_x, center_y, angle, speed, objetivo):
        super().__init__(textura, scale, center_x=center_x, center_y=center_y, angle=angle, speed=speed, objetivo=objetivo)

        if textura:
            self.texture = textura
            w, h = self.texture.width * self.scale, self.texture.height * self.scale
            self.set_hit_box([
                (-w / 5, -h / 3),
                (w / 5, -h / 3),
                (w / 5, h / 3),
                (-w / 5, h / 3)
            ])

    def update(self):
            super().update()

class Telar(Proyectil):
    def __init__(self, textura, scale, center_x, center_y, angle, speed, objetivo):
        super().__init__(textura, scale, center_x=center_x, center_y=center_y, angle=angle, speed=speed, objetivo=objetivo)

        if textura:
            self.texture = textura
            w, h = self.texture.width * self.scale, self.texture.height * self.scale
            self.set_hit_box([
                (-w / 4, -h / 4),
                (w / 4, -h / 4),
                (w / 4, h / 4),
                (-w / 4, h / 4)
            ])

    def update(self):
            super().update()
