import arcade

from resources.sounds.Sounds import attack_sound
from rpg.constants import stats
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
        self.attack_timer3 = 0
        self.pattern_timer = 0  #tiempo entre patrones
        self.combat_timer = 0 #tiempo del combate en general
        self.current_pattern = ""
        self.player_damage = 20
        self.final_pattern = False

        #reseteo la vida y la convicción del boss al empezar
        self.boss.boss_hp = self.boss.boss_max_hp
        self.boss.convencido = 0
        #selecciona el primer patron del combat
        if self.map == "mapa_boss_slime":
            self.choose_next_pattern()
        elif self.map == "mapa_boss_fantasma":
            self.current_pattern = "Tp"

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
        print("convencido:" + str(self.boss.convencido))
        self.boss.convencido += 1
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
                decision(self.botones, lambda: self.attack(), lambda: self.persuadir(),lambda: self.mochila(), self.dialog_manager, self.boss)
                self.pattern_timer = self.boss.pattern_duration +1
                GameView.state = "Dialog"
                self.choose_next_pattern()


        if self.state == "fight": #esto ocurre cuando estamos luchando
            self.attack_timer += delta_time
            self.attack_timer2 += delta_time
            self.attack_timer3 += delta_time
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
            stats["HP"] = stats["HP_MAX"]
            GameView.state = "Locked"
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
        elif self.map == "mapa_boss_fantasma": #si es el fantasma
            if self.boss.convencido < 2:
                if 30 < self.boss.boss_hp < 70:
                    self.current_pattern = "Summon"
                elif 10 < self.boss.boss_hp <= 30:
                    self.current_pattern = "Summon and Dash"
                elif self.boss.boss_hp <= 10:
                    self.current_pattern = "Dash"
                else:
                    if self.current_pattern == "Tp":
                        self.current_pattern = "Dash"
                    else:
                        self.current_pattern = "Tp"
            else:
                self.current_pattern = random.choice(["Dash", "Summon", "Tp"])





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
        elif self.current_pattern == "Tp":
            if self.attack_timer > 0.9:
                self.boss.stop()
                self.boss.random_tp(self.boss)
                self.attack_timer = 0
        elif self.current_pattern == "Dash":
            if self.attack_timer < 0.5:
                self.boss.stop()
                self.boss.random_tp(self.boss)
                self.attack_timer = 0.5
            if 1.5 < self.attack_timer < 2:
                self.boss.attack_dash(self.player, self.boss, 8)
                self.attack_timer = 2
            if 3.3 < self.attack_timer < 4.3:
                self.boss.stop()
                self.boss.random_tp(self.boss)
                self.attack_timer = 4.3
            if 6 < self.attack_timer < 6.5:
                self.boss.attack_dash(self.player, self.boss, 8)
                self.attack_timer = 6.5
        elif self.current_pattern == "Summon":
            if self.attack_timer < 0.2:
                self.boss.stop()
                self.boss.teleport(190, -60)
                self.boss.animacion_actual = 3
            elif self.attack_timer > 1.3:
                self.boss.attack_summon(self.player,self.peligros_list)
                self.attack_timer = 0.2
        elif self.current_pattern == "Summon and Dash":
            if 2 < self.attack_timer3 < 7:
                if self.attack_timer > 0.8:
                    self.boss.stop()
                    self.boss.random_tp(self.boss)
                    self.attack_timer = 0
            elif self.attack_timer2 > 1.65:
                self.boss.attack_summon(self.player,self.peligros_list)
                self.attack_timer2 = 0
            if self.attack_timer3 > 7:
                self.boss.attack_dash(self.player, self.boss, 7)
                self.attack_timer3 = 0




    def check_boss_health(self):
        if self.boss.boss_hp <= 0:
            self.boss.death = True
            self.colocar_los_bosses()
            self.state = "win"

        elif self.boss.boss_anger <= self.boss.convencido:
            self.colocar_los_bosses()
            self.state = "win"

