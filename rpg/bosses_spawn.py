import arcade




def colocar_boss(mapa,lista_peligros,boss):
    from rpg.views.game_view import GameView
    if not boss.death:
        if mapa == "mapa_boss_slime":
            if boss not in lista_peligros:
                GameView.state = "Locked"
                lista_peligros.append(boss)
        else:
            if boss in lista_peligros:
                lista_peligros.remove(boss)
    else:
        if boss in lista_peligros:
            lista_peligros.remove(boss)


def coloca_boses(mapa,lista_peligros,slime):   #funcion que hace spawnear al boss, se usa en el gameview
    lista_peligros.clear()
    colocar_boss(mapa, lista_peligros, slime)