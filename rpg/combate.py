import arcade

from resources.sounds.Sounds import attack_sound
from rpg.decisiones import decision
from rpg.musica import stop_music
from rpg.views.settings_view import SettingsView


class CombatManager:

    def __init__(self, player, boss, peligros_list, map, botones, colocar_los_bosses, dialog_manager, inventory_view):
        self.player = player
        self.boss = boss
        self.peligros_list = peligros_list
        self.map = map
        self.botones = botones
        self.colocar_los_bosses = colocar_los_bosses
        self.dialog_manager = dialog_manager
        self.inventory_view = inventory_view
        self.state = "fight"
        self.attack_timer = 0  #tiempo entre ataques de un patron
        self.attack_timer2 = 0
        self.pattern_timer = 0  #tiempo entre patrones
        self.combat_timer = 0 #tiempo del combate en general
        self.current_pattern = ""
        self.player_damage = 20
        self.convencido = 0
        self.final_pattern = False

        #reseteo la vida del boss al empezar
        self.boss.boss_hp = self.boss.boss_max_hp
        #selecciona el primer patron del combat
        self.choose_next_pattern()

    # funciones para la decisión en combate
    def attack(self):
        from rpg.views.game_view import GameView
        self.boss.boss_hp -= self.player_damage
        arcade.play_sound(attack_sound, volume=0.4 * SettingsView.v_ef)
        self.boss.take_damage()
        print(self.boss.boss_hp)
        self.combat_timer = 0
        self.state = "fight"
        GameView.state = "Combat"

    def persuadir(self):
        from rpg.views.game_view import GameView
        print("convencido:" + str(self.convencido))
        self.convencido += 1
        self.combat_timer = 0
        self.state = "fight"
        GameView.state = "Combat"

    def mochila(self):
        from rpg.views.game_view import GameView
        print("inventory screen:")
        self.state = "fight"
        self.inventory_view()
        self.combat_timer = 0


    def update(self, delta_time):
        from rpg.views.game_view import GameView
        self.combat_timer += delta_time
        if self.combat_timer > self.boss.fase_duration: #el tiempo de cada fase
            self.state = "espera"
            if self.combat_timer > self.boss.fase_duration + 3 and self.state != "dialog":
                from rpg.views.game_view import GameView

                self.state = "dialog"
                decision(self.botones, lambda: self.attack(), lambda: self.persuadir(),lambda: self.mochila(), self.dialog_manager)
                self.pattern_timer = self.boss.pattern_duration +1
                GameView.state = "Dialog"


        if self.state == "fight": #esto ocurre cuando estamos luchando
            self.attack_timer += delta_time
            self.attack_timer2 += delta_time
            self.pattern_timer += delta_time

            if self.pattern_timer > self.boss.pattern_duration:
                if not self.final_pattern:
                    self.choose_next_pattern()
                    self.attack_timer = 0
                    self.attack_timer2 = 0
                    self.pattern_timer = 0

            self.run_current_pattern()

        self.check_boss_health() #revisa la vida del boss, para ver si está muerto y eso
        if self.state == "win":
            GameView.state = "Exploration"
            stop_music()


    def choose_next_pattern(self):      #elige el siguiente patron
        import random
        if self.map == "mapa_boss_slime": #si es el slime
            if self.state == "fight":
                self.boss.set_animation("shoot")  #animación de atacar

            if self.boss.boss_hp <= self.boss.boss_max_hp/4:
                self.current_pattern = "rain and crush"
                self.final_pattern = True
            else:
                self.current_pattern = random.choice(["rain", "crush"])



    def run_current_pattern(self):
        #Patrones Slime
        if self.current_pattern == "rain":
            if self.attack_timer > 0.3:
                if self.pattern_timer<5:
                    self.boss.attack_rain(self.peligros_list, self.player)
                    self.attack_timer = 0
        elif self.current_pattern == "crush":
            if self.attack_timer > 1.4:
                self.boss.attack_crush(self.peligros_list,self.player)
                self.attack_timer = 0
        elif self.current_pattern == "rain and crush":
            if self.combat_timer < 19:
                if self.attack_timer > 0.8:
                    self.boss.attack_rain2(self.peligros_list, self.player)
                    self.attack_timer = 0
            if self.attack_timer2 > 3:
                self.boss.attack_crush(self.peligros_list,self.player)
                self.attack_timer2 = 0

    def check_boss_health(self):
        if self.boss.boss_hp <= 0:
            self.boss.death = True
            self.colocar_los_bosses()
            self.state = "win"

        elif self.boss.boss_anger <= self.convencido:
            self.state = "win"

