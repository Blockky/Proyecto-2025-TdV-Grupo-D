# Memoria

## Nombre del videojuego: Beast and Bonds



## 1. Miembros del equipo que han participado y sus respectivos roles finales


- **Pablo García Hernández** - 1° GIC  
  _Jefatura de proyecto, Programación, Diseño gráfico_
  
- **David Salgado** - 1º GISI  
  _Diseño de niveles, Pruebas, Programación_
  
- **Roberto Pais Bustamante** - 1º GIC  
  _Programación, Diseño de niveles, Pruebas_
  
- **Carmen Dávila Montero** - 1º GII  
  _Diseño Gráfico, Diseño de niveles_
  
- **Luka Luraschi** - 1º GII  
  _Diseño de niveles, Pruebas, Diseño Gráfico_
  
- **Sergio Peiteado Sánchez** - 1º GII  
  _Programación, Sonido, Pruebas_

---


## 2. Gestión del equipo y reparto de las tareas

- En el arranque del proyecto, 1 mes y semanas antes de la entrega, se repartieron
diferentes tareas a los miembros del equipo, las cuales se pudieran de hacer de forma paralela
sin depender de que una estuviera terminada para poder empezar la siguiente. Con esto se consiguió
que un trabajo dinámico y coordinado.
- Las primeras tareas del juego consistieron principalmente en el diseño de tanto los niveles como los personajes.
Estas tareas fueron repartidas de la siguiente manera:
  - Luka Luraschi se encargó de las salas de exploración y parte de los sprites de los bosses (slime, campana, ángel)
  - Cármen Dávila realizó el diseño de la tienda y del resto de sprites de bosses (robot, araña, fantasma)
  - David Salgado diseñó las salas de combate del juego
  - Pablo García realizó el diseño del personaje principal
  - Y Roberto Pais hizo las salas de inicio y final del juego


- Mientras los diseñadores de niveles y parte de los de diseño gráfico empezarón con sus tareas, también se inició
el proceso de la programación y de implementación de sonido. El miembro Sergio Peiteado implementó el sistema de vida del juego,
haciendo que se dibujasen en la pantalla unos corazones que indicasen la vida del personaje. Además, configuró objetos que pudieran
reducir la vida del personaje.
- Durante las semanas intermedias se metió más mano al apartado del código. Se implementó un nuevo sistema de inventario en el que
se puede hacer uso de pociones que curan la vida del personaje (tarea hecha por Roberto).
- También se intentó implementar los mapas hechos en tiled en el código, hecho el cual duró bastante en realizarse de forma correcta,
ya que no se podía abrir el juego en el mapa correspondiente, o si se conseguía, el juego se cerraba por un error (no se configuraba el fondo).
Además, ciertos tilesets se subieron en formatos incorrectos (.tsx) en vez de en (.json). Y la detección de colisiones con las paredes
no se implementó de forma correcta, ya que faltaba por configurar los nombres de las capas no traspasables.
- Paralelamente, se empezó a diseñar la lógica de los combates. Pablo García creó un mini proyecto temporal en el que con sprites de prueba
cuando el sprite que se controla interactuaba con otro (pulsando a la E) se iniciaba un diálogo y tras ello empezaba una secuencia de ataques.
Esta fue la base para implementar los diálogos y combates en nuestro juego. Cármen se encargó de redactar e implementar en el juego los diálogos
con los personajes (esto consistió esencialmente en crear listas de cadenas que contiene los diálogos) y en implementar una caja de diálogo en el
que apareciera el texto deseado.
- En cuanto a la secuencia de ataques, Sergio diseñó secuencias de proyectiles originales en los combates contra el slime, el fantasma y la campana,
terminándose de implementar también por Pablo con el robot, la araña y el boss final, además de diseñar los proyectiles. Sergio también se encargó
de implementar los botones de la toma de decisiones en los combates (atacar/hablar/usar inventario).

---

## 3. Evaluación del proyecto con respecto al GDD

En una primera instancia se tuvieron varias ideas a implementar en el juego, las cuales no se han podido lograr.

- Se quiso que la toma de decisiones afectase al final del juego, habiendo dos finales (dependiendo de si perdonabas o matabas a los bosses). Además,
dependiendo de si matabas o perdonabas a cierto boss, este te daría una llave para acceder por una puerta del mapa u otra (función que no se implementó).
- La tienda al final no se pudo implementar de la forma deseada. La primera intención era que hubiera un gato en las diferentes tiendas del mapa
que te vendiera distintos tipos de items. Lo que se implementó al final fue una tienda a la cual se puede acceder desde el menú del juego.
- Tampoco se implementó el sistema de economía, es decir, puntos que se pudieran obtener al final de los combates.
- No se añadieron puzzles en los mapas de exploración, como por ejemplo pulsar botones para poder acceder a la siguiente sala. No obstante,
como los mapas son grandes y con pasadizos pequeños, esto ya puede contar como puzzle, ya que no es tan fácil determinar cómo se accede a la siguiente sala,
ya que hay vallas que impiden pasar, fuentes de agua que funcionan como puente de acceso o puentes para cruzar unos riachuelos.


En general, la parte de los combates a lo estilo bullethell se pudo implementar con éxito y la toma de decisiones, siendo estos los factores más
importantes del juego. Teniendo esto en cuenta y las ideas que no se pudieron implementar, hablando de forma autocrítica, gran parte y esencia del juego
se asemeja al presentado en el GDD.

---

## 4. Consideraciones de interés

El reparto de las tareas siempre se hizo teniendo en cuenta el grado de los miembros. 
- Luka Luraschi fue el que mayores aportaciones hizo en cuanto a los diseños de los niveles (esto también fue por voluntad propia de él
y por tener más experiencia con este tipo de diseños) respetando a todo el equipo, es decir, que los demás diseñadores de niveles hicieron sus
correspondientes aportaciones
- Durante los fallos a la hora de implementar las salas de combate, el jefe de proyecto compartió la solución de parte de los errores y conectó
al equipo para que se ayudasen entre ellos, ya que algunos tenían más complicaciones que otros, pero al final todos pudieron realizar sus tareas con éxito.
- También se aseguró de que todo el equipo aportara alguna parte de código, es decir, que trabajasen en el apartado de programación. A los que menos apaño
tuvieran con el código se le entregaron tareas más cómodas como la implementación de diálogos o la transición de puertas.

## 5. Notas para el instructor

En el combate contra el robot computador, los proyectiles que te lanza este son módulos de memoria RAM.
