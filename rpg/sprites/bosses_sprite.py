
import arcade
import rpg.constants as constants
from resources.sounds.Sounds import ghost_sound
from rpg.sprites.peligros import Proyectil, Esbirro
from rpg.views.settings_view import SettingsView
import math

ANIMATION_SPEED = 0.1  # en segundos por frame

class Boss(arcade.Sprite):
    def __init__(self, spritesheet_path,columnas,filas, frame_width, frame_height, position, scale, hp, anger):
        super().__init__(scale = scale)
        self.columnas = columnas
        self.filas = filas
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = self.columnas * self.filas
        self.boss_max_hp = hp
        self.boss_hp = self.boss_max_hp
        self.boss_anger = anger
        self.convencido = 0
        self.textures = []
        self.flash_count = 0
        self.flashing = False
        self.death = False
        self.show_health_bar = False  # si se dibuja o no la barra de vida

        for row in range(self.filas):
            for col in range(self.columnas):
                x = col * self.frame_width
                y = row * self.frame_height

                texture = arcade.load_texture(spritesheet_path,x=x,y=y,width=self.frame_width,height=self.frame_height)
                self.textures.append(texture)

        self.center_x, self.center_y = position
        self.current_texture_index = 0
        self.texture = self.textures[self.current_texture_index]
        self.time_since_last_change = 0
    #Barra de vida de los bosses
    def draw_health_bar(self):
        if not self.show_health_bar:
            return  # No se dibuja durante el parpadeo

        # Tamaño y posición de la barra
        bar_width = 500
        bar_height = 15
        hp_percentage = self.boss_hp / self.boss_max_hp
        health_width = bar_width * hp_percentage

        x = constants.SCREEN_WIDTH // 2
        y = 30

        arcade.draw_rectangle_filled(x, y, bar_width, bar_height, arcade.color.GRAY) # el fondo
        if self.boss_hp > 0:
            arcade.draw_rectangle_filled(x - (bar_width - health_width) / 2, y, health_width, bar_height,arcade.color.RICH_CARMINE) #el relleno (la vida)
        arcade.draw_rectangle_outline(x, y, bar_width + 1, bar_height + 1, arcade.color.WHITE) # el borde

    def update_animation(self, delta_time: float = 1/60):
        self.time_since_last_change += delta_time
        if self.time_since_last_change > ANIMATION_SPEED:
            self.time_since_last_change = 0
            self.current_texture_index = (self.current_texture_index + 1) % len(self.textures)
            self.texture = self.textures[self.current_texture_index]

    #representa que ha recibido daño
    def take_damage(self):
        if not self.flashing:
            self.flash_count = 0
            self.flashing = True
            arcade.schedule(self.flash_effect, 0.1)

    def flash_effect(self, delta_time):
        # alpha entre opaco y transparente
        self.alpha = 90 if self.alpha == 255 else 255
        self.show_health_bar = not self.show_health_bar #La barra también parpadea
        self.flash_count += 1

        if self.flash_count >= 6:  # 3 flashes
            self.alpha = 255
            if self.boss_hp > 0 and self.boss_anger > self.convencido:
                self.show_health_bar = True
            arcade.unschedule(self.flash_effect)
            self.flashing = False


class Slime(Boss):
    def __init__(self, idle_spritesheet, special_spritesheet,columnas, filas, frame_width, frame_height, position, scale, hp, anger):
        super().__init__(idle_spritesheet,columnas,filas, frame_width, frame_height, position, scale, hp, anger)
        self.pattern_duration = 7 #lo que dura cada patron de ataque del boss
        self.fase_duration = 21 #lo que dura cada fase del combate del boss

        self.textura_gota = arcade.load_texture("../resources/characters/Slime/Slime_Sprites.png", x=295, y=40, width=20, height=15)

        # Tiene dos animaciones
        self.animations = {
            "idle": self.textures,
            "shoot": []
        }

        # Cargar animación shoot
        num_special_frames = 8 #esta animación tiene distintos frames
        for col in range(num_special_frames):
            x = col * self.frame_width
            y = 2 * self.frame_height  # tercera fila
            tex = arcade.load_texture(special_spritesheet, x=x, y=y, width=self.frame_width, height=self.frame_height)
            self.animations["shoot"].append(tex)

        self.one_shot_animations = {"shoot"}
        self.current_animation = "idle"
        self.current_texture_index = 0
        self.time_since_last_change = 0

    def set_animation(self, name):
        if name in self.animations and name != self.current_animation:
            self.current_animation = name
            self.current_texture_index = 0
            self.time_since_last_change = 0
            self.texture = self.animations[name][0]

    def update_animation(self, delta_time: float = 1 / 60):
        self.time_since_last_change += delta_time
        if self.time_since_last_change > ANIMATION_SPEED:
            self.time_since_last_change = 0

            frames = self.animations[self.current_animation]
            if self.current_texture_index + 1 < len(frames):
                self.current_texture_index += 1
            else:
                if self.current_animation in self.one_shot_animations:
                    self.set_animation("idle")
                    return
                else:
                    self.current_texture_index = 0

            self.texture = frames[self.current_texture_index]
            self.set_hit_box(self.texture.hit_box_points) #actualiza la hitbox


    #Patrones de ataque del slime:

    def attack_rain(self, peligros_list, player):
        import random
        random_x = random.randint(0, constants.SCREEN_WIDTH-900)

        gota = Proyectil(self.textura_gota,2,random_x,430,270,1.3,player)
        peligros_list.append(gota)

    def attack_rain2(self, peligros_list, player):
        import random
        random_x = random.randint(200, constants.SCREEN_WIDTH-550)
        random_x2 = random.randint(450, constants.SCREEN_WIDTH - 550)

        gota = Proyectil(self.textura_gota,2,random_x,420,210,0.9,player)
        gota2 = Proyectil(self.textura_gota, 2, random_x2, 300, 210, 0.9, player)
        peligros_list.append(gota)
        peligros_list.append(gota2)

    def attack_crush(self, peligros_list, player):
        import random
        random_num = random.randint(0,1)
        if random_num == 0:
            gota_izq = Proyectil(self.textura_gota, 2, player.center_x -250, player.center_y + 12, 0, 6, player)
            gota_dere = Proyectil(self.textura_gota, 2, player.center_x +250, player.center_y - 12, 180, 7, player)
            peligros_list.append(gota_izq)
            peligros_list.append(gota_dere)
        if random_num == 1:
            gota_arrib = Proyectil(self.textura_gota, 2, player.center_x + 11, player.center_y +250, 270, 7, player)
            gota_abaj = Proyectil(self.textura_gota, 2, player.center_x - 12, player.center_y -250, 90, 6, player)
            peligros_list.append(gota_abaj)
            peligros_list.append(gota_arrib)



class Fantasma(Boss):
    def __init__(self, spritesheet_path, columnas, filas, frame_width, frame_height, position, scale, hp, anger):
        self.spritesheet_path = spritesheet_path
        super().__init__(spritesheet_path, columnas, filas, frame_width, frame_height, position, scale, hp, anger)
        self.start_x = self.center_x
        self.start_y = self.center_y
        self.pattern_duration = 5  # lo que dura cada patron de ataque del boss
        self.fase_duration = 30  # lo que dura cada fase del combate del boss
        self.animaciones = self._cargar_animaciones()
        self.animacion_actual = 0
        self.current_frame = 0
        self.time_since_last_change = 0
        self.texture = self.animaciones[self.animacion_actual][self.current_frame]
        self.attack_timer = 0
        self.shout = True

        #Movimiento
        self.direction = 0
        self.speed = 0
        self.radianes = math.radians(self.direction)
        self.change_x = math.cos(self.radianes) * self.speed
        self.change_y = math.sin(self.radianes) * self.speed
        self.follow = False

    def update(self):
        # Movimiento
        self.center_x += self.change_x
        self.center_y += self.change_y


    def _cargar_animaciones(self):
        """Carga las animaciones por fila."""
        animaciones = []
        for row in range(self.filas):
            fila_anim = []
            for col in range(self.columnas):
                x = col * self.frame_width
                y = row * self.frame_height
                texture = arcade.load_texture(self.spritesheet_path, x=x, y=y, width=self.frame_width, height=self.frame_height)
                fila_anim.append(texture)
            animaciones.append(fila_anim)
        return animaciones

    def cambiar_animacion(self, nueva_fila):
        """Cambia a una nueva animación (fila de sprites)."""
        if 0 <= nueva_fila < self.filas:
            self.animacion_actual = nueva_fila
            self.current_frame = 0
            self.time_since_last_change = 0
            self.texture = self.animaciones[self.animacion_actual][self.current_frame]

    def update_animation(self, delta_time: float = 1/60):
        self.time_since_last_change += delta_time
        if self.time_since_last_change > ANIMATION_SPEED:
            self.time_since_last_change = 0
            self.current_frame = (self.current_frame + 1) % len(self.animaciones[self.animacion_actual])
            self.texture = self.animaciones[self.animacion_actual][self.current_frame]

    def teleport(self, x, y):
        self.center_x = x
        self.center_y = y

    def move(self,speed,angle):
        self.speed = speed
        self.direction = angle
        self.radianes = math.radians(self.direction)
        self.change_x = math.cos(self.radianes) * self.speed
        self.change_y = math.sin(self.radianes) * self.speed

    def stop(self):
        self.change_x = 0
        self.change_y = 0

    def random_shout(self):
        import random
        random_num = random.randint(0, 1)

        if self.shout and random_num == 1:
            arcade.play_sound(ghost_sound, volume=0.4 * SettingsView.v_ef)
            self.shout = False
        else:
            self.shout = True

    #self.teleport(random_num2, -60)  # abajo
    #fantasma.animacion_actual = 3

    def random_tp(self,fantasma):
        import random
        random_num = random.randint(0, 2)
        random_num2 = random.randint(30, 370)
        self.random_shout()

        if random_num == 0:
            self.teleport(-70, random_num2) #izquierda
            fantasma.animacion_actual = 2
        elif random_num == 1:
            self.teleport(450, random_num2)  # derecha
            fantasma.animacion_actual = 1
        elif random_num == 2:
            self.teleport(random_num2, 460)  # arriba
            fantasma.animacion_actual = 0

    def attack_dash(self, player, fantasma, speed):
        # Calcula diferencia en coordenadas
        dx = player.center_x - fantasma.center_x
        dy = player.center_y - fantasma.center_y

        # Calcula ángulo en radianes y convierte a grados
        angulo_radianes = math.atan2(dy, dx)
        angulo_grados = math.degrees(angulo_radianes)

        velocidad = speed

        self.random_shout()

        if fantasma.animacion_actual == 2 and dx > 0:  # mirando a la derecha
            self.move(velocidad, angulo_grados)
        elif fantasma.animacion_actual == 1 and dx < 0:  # mirando a la izquierda
            self.move(velocidad, angulo_grados)
        elif fantasma.animacion_actual == 0 and dy < 0:  # mirando hacia arriba
            self.move(velocidad, angulo_grados)

    def attack_summon(self, player, peligro_list):
        import random
        random_num = random.randint(30, 370)
        random_num2 = random.randint(0, 1)
        if random_num2 == 0:
            esbirro1 = Esbirro("../resources/characters/Enemy/Enemy 16-1.png",1,-30,random_num,180,2,player,True)
        else:
            esbirro1 = Esbirro("../resources/characters/Enemy/Enemy 16-1.png", 1, 420, random_num, 180, 2, player, True)
        peligro_list.append(esbirro1)