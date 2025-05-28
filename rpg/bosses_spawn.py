import arcade




def colocar_boss(mapa,lista_peligros,boss, mapa_boss):
    from rpg.views.game_view import GameView
    if not boss.death:
        if mapa == mapa_boss:
            if boss not in lista_peligros:
                if mapa != "salaExp_S1":
                    GameView.state = "Locked"
                lista_peligros.append(boss)
        else:
            if boss in lista_peligros:
                lista_peligros.remove(boss)
    else:
        if boss in lista_peligros:
            lista_peligros.remove(boss)


def coloca_boses(mapa,lista_peligros, angel, slime, angel2, angel3):   #funcion que hace spawnear al boss, se usa en el gameview
    lista_peligros.clear()
    colocar_boss(mapa, lista_peligros, slime, "mapa_boss_slime")
    colocar_boss(mapa, lista_peligros, angel, "StartingRoomMap")
    if not slime.death: #para que reaparezca el angel 2 solo si el slime está vivo
        colocar_boss(mapa, lista_peligros, angel2, "mapa_boss_slime")
    colocar_boss(mapa, lista_peligros, angel3, "salaExp_S1")
