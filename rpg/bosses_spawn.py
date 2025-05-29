import arcade



def colocar_boss(mapa,lista_peligros,boss, mapa_boss):
    from rpg.views.game_view import GameView
    boss.show_health_bar = False #desaparece la barra de vida
    if not boss.death:
        if mapa == mapa_boss:
            if boss.convencido >= boss.boss_anger:
                GameView.state = "Exploration"
                lista_peligros.append(boss)
            elif boss not in lista_peligros:
                GameView.state = "Locked"
                lista_peligros.append(boss)

            if mapa == "mapa_boss_fantasma":
                boss.stop()
                boss.teleport(boss.start_x, boss.start_y)
        else:
            if boss in lista_peligros:
                lista_peligros.remove(boss)
    else:
        if boss in lista_peligros:
            lista_peligros.remove(boss)
        GameView.state = "Exploration"


def coloca_boses(mapa,lista_peligros, angel, slime, angel2, angel3, fantasma, aranna):   #funcion que hace spawnear al boss, se usa en el gameview
    lista_peligros.clear()
    colocar_boss(mapa, lista_peligros, slime, "mapa_boss_slime")
    colocar_boss(mapa, lista_peligros, angel, "StartingRoomMap")
    if not slime.death: #para que reaparezca el angel 2 solo si el slime está vivo
        colocar_boss(mapa, lista_peligros, angel2, "mapa_boss_slime")
    colocar_boss(mapa, lista_peligros, angel3, "salaExp_S1")
    colocar_boss(mapa, lista_peligros, fantasma, "mapa_boss_fantasma")
    fantasma.animacion_actual = 0
    colocar_boss(mapa, lista_peligros, aranna, "mapa_boss_arana")
