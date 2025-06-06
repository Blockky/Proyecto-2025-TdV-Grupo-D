import arcade

from resources.sounds import Sounds

#reproduce la música si no se está reproduciendo ya
def musc_ambiente(musica, volumen):
    from rpg.views.settings_view import SettingsView
    global current_music, current_player

    if current_music != musica:
        if current_player:
            current_player.delete()
        current_player = arcade.play_sound(musica, looping=True, volume=volumen * SettingsView.v_music)
        current_music = musica

current_music = None #musica usandose
current_player = None #reproductor usandose

def stop_music():
    if current_player:
        current_player.delete()


#reproduce la música correspondiente en cada mapa
def reproduce_musica(mapa):
    global current_music
    if mapa == "StartingRoomMap" or mapa == "salaExp_I":
        musc_ambiente(Sounds.inicio_music, 0.7)
    elif mapa == "salaExp_S1" or mapa == "salaExp_S2":
        musc_ambiente(Sounds.slime_music, 0.5)
    elif mapa == "salaExp_A1" or mapa == "salaExp_A2":
        musc_ambiente(Sounds.arana_music, 0.5)
    elif mapa == "salaExp_F1" or mapa == "salaExp_F2":
        musc_ambiente(Sounds.fantasma_music, 0.5)
    elif mapa == "salaExp_C" or mapa == "salaExp_B":
        musc_ambiente(Sounds.campanabosque_music, 0.5)
    elif mapa == "salaExp_R1" or mapa == "salaExp_R2":
        musc_ambiente(Sounds.robot_music, 0.5)
    elif mapa == "salaExp_U":
        musc_ambiente(Sounds.angel_music, 0.5)


