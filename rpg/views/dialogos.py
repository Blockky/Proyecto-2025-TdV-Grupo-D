#dialogos de los personajes

#Angel al principio del juego. Primera vez que nos lo encontramos
angel = ["¡Buenas viajero!",
         "¿Qué dices que estás perdido?¿Y no sabes cómo has llegado aquí?",
         "¡No pasa nada! Yo también estoy perdido así que nos podemos ayudar mutuamente. ¿Eh, qué dices?", #ver si poner aqui toma de decisiones
         "Bien… Por lo poco que he podido explorar, he averiguado que hay una especie de recompensa al final de esta mazmorra. Así que ese puede ser nuestro escape.",
         "Eso sí, mientras estaba investigando he escuchado algunos ruidos, no sé…eran como ¿monstruos?. Aunque creo que ha sido mi imaginación, o eso espero.",
         "De todas formas, no le demos más vueltas. Cuanto antes entremos, antes saldremos y averiguaremos que pasa.",
        "¡Vamos allá!"]
angel_loop = ["Nos vemos dentro."] #se repite tras haber hablado ya

#segunda conversacion del angel al llegar a la sala donde está el slime(que no habla al ser un combate introductorio
angel2 = ["Vaya… Sinceramente, no esperaba esto. Espera. Qué es eso que está ahí?",
          "¡¿Es un monstruo?! ¡Encárgate de él!"]

#conversación durante el combate del slime
angel_slime1 = ["Ahora es tu oportunidad, atácale mientras está descansando."]
angel_slime2 = ["Ya falta poco.",
                "Pero ten cuidado al seguir atacándole.",
                "Siempre se resisten más cuando están cerca de morir."]
angel_slime3 = ["Sigue atacandole."]
angel_slime_dialogar = ["No sirve de nada hablarle a un slime, no son lo suficientemente inteligentes.",
                        "Auque es cierto que suele ser una buena técnica para salvarte sin enfadar a tu oponente."]


#conversacion con el angel al finalizar el combate
angel3 = [" Uf… Por poco",
          "¡Muy buena esa! Estuvo increíble",
          "Aunque ese monstruo… Probablemente haya más esparcidos por la mazmorra. Así que no nos confiemos",
          "Yo creo que lo mejor será separarnos por el momento para poder explorar más a fondo. Nos reuniremos más adelante para compartir nuestros descubrimientos. No te preocupes por mí, puedo con todo.",
          "¡Vamos a ello!"]
angel3_loop = ["No te preocupes por mí, puedo con todo."] #se repite tras haber hablado ya

#Conversación con el de la tienda (será siempre la misma)
gato = ["¡Ey, tú! ¡Sí, tú! ¡Bienvenido a mi tienda!",
        "Aquí podrás encontrar todo lo que necesitas para tu gran aventura. Desde armas, pociones…¡de todo!",
        "Así que echa un vistazo y me dices, ¿vale?"]
#si compras algo
gato_comprar= ["Gracias. Y vuelve pronto, ¿vale?"]
#si no compras
gato_no_comprar = ["Pues adiós"]


#Diálogos del fantasma
#antes de iniciar el combate
fantasma = ["¡Boo! Jejejejeje. ¿A qué te has asustado?",
            "¿No? Bueno, da igual, porque de aquí no podrás pasar"]

fantasma_dialogar1 = ["Se lo que intentas",
                      "¿Intentas que te deje pasar verdad?",
                      "¿Pues sabes que?",
                      "Eso no va a ocurrir!"]
fantasma_dialogar3 = ["Puede que estés empezando a caerme mejor",
                      "Uy, ¿He dicho eso en voz alta?"]
fantasma_dialogar2 = ["¡Paraaaa!",
                      "Estás quitandole la gracia a acabar con tigo."]
fantasma_dialogar4 = ["Vale, tu ganas."]

#si se deja vivo -> consejos futuros
fantasma2 = ["Supongo que gracias por no haberme matado",
             "Como agradecimiento, te voy a dar alguna pista.",
             "Esta mazmorra es bastante extraña como ya has podido ver, lo único que te puedo decir es que no puedes confiar en nadie.",
             "En. Nadie. ¿Entendido?",
             "Pues eso, que te vaya bien. Cualquier cosa vuelve aquí si necesitas algo más."]
#lo que va a decir si vuelves será siempre lo mismo:
fantasma3 = ["¿Ya te he dicho q no confíes en nadie en este sitio, no?"]


#Diálogos de la araña
#antes de iniciar el combate
aranna = ["¿Pero qué tenemos por aquí?",
          "Ha pasado mucho tiempo desde que él trajo a un nuevo viajero.",
          "No te preocupes, nos lo vamos a pasar muy bien."]
#si se deja vivo -> seguirá siendo hostil aunque ya no ataca
aranna2 = ["Aunque me hayas dejado vivir, no te daré las gracias.",
           "Así que no te voy a dar mi ayuda.",
           "Vete."]


#Diálogos de la campana // sombra
#antes de iniciar el combate
campana = ["Campana: ¡Bienvenido! Hace mucho tiempo que no venía alguien nuevo por aquí.",
           "Sombra: No es bienvenido aquí nadie, es un enemigo.",
           "Campana: Lo siento... Yo no quería hacer esto."]
#si se deja vivo -> la campana intentará ayudarte mientras que la sombra no
campana2 = ["Sombra: No te voy a ayudar en nada. Estás perdiendo tu tiempo.",
            "Campana: ¡Muchas gracias por dejarme vivir! Te ayudaré en todo lo posible, aunque no conozca muy bien este lugar."]
campana_ayuda = ["Campana: Bien. Una de las cosas que sé es que hay una araña rondando por aquí que no te va a ayudar en nada. Por lo que no pierdas tu tiempo.",
                 "Campana: ¡Y otra cosa! Creo que hay alguien quien podría ayudarte a entender mejor qués es este sitio.",
                 "Campana: La cosa es que no me acuerdo de quién es. Lo siento."]

#Diálogos del robot
#antes de iniciar el combate
robot = ["Se ha detectado un sujeto desconocido en el entorno.",
         "Analizando objetivo.",
         "Análisis completado. Resultado: enemigo.",
         "Comenzar protocolo de ataque."]
#si se deja vivo -> ayudas para la exploración y la mazmorra, jefe final
robot2 = ["Se percibe una presencia extraña al final de esta mazmorra",
          "Investigación en curso. Espere un momento.",
          "Atención a detalles. No confiar en sujetos con los que se ha mantenido una conversación inicialmente.",
          "Para descubrirlo, siga superando los desafíos.",
          "Eso es todo."]

#Diálogos del jefe final[ángel - demonio], la revelación
#antes de iniciar el combate -> revelación
angel4 = ["¡Hola otra vez, querido amigo!",
          "Hemos llegado los dos al final de la mazmorra, ¿no es eso bueno?",
          "Bueno… ¿Te acuerdas que te dije que descubrí que había una recompensa que nos permitiría salir de aquí?",
          "Pues eso era mentira. La verdad nunca pensé que fuera tan fácil mentir a un humano. Pero ha estado bastante gracioso",
          "Ahora sí, dejémonos de tonterías"]
#se pasa a demonio
demonio = ["¿No te parecía extraño que desde un principio yo supiera sobre una supuesta recompensa si acababa de llegar aquí al igual que tú?",
           "¿Ni que hubiera una mazmorra así con monstruos en mitad de la nada?",
           "En verdad, esperaba más. Pero bueno, que se le va a hacer.",
           "No te preocupes, aventurero. Tu gran aventura acaba aquí."]
#tras el combate antes de morir
demonio2 = ["Esto... Esto, es inesperado...",
            "Al final... has logrado alcanzar tu victoria... aventurero.",
            "Más adelante... Te espera lo que has estado buscando.",
            "Adiós..."]