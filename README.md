# Defensa y Asalto de Base

Proyecto del curso Introduccion a la Programacion (Modalidad Live Learning),
Tecnologico de Costa Rica.

## Integrantes

- Allem Alejandro Mena Ruiz
- Joel Alpizar Ramirez

## Descripcion

Juego de estrategia para dos jugadores. Un jugador es el defensor y debe
construir una base con muros y torres defensivas; el otro jugador es el
atacante y debe destruir la base central usando distintas unidades. El
juego se juega por rondas y el primero en ganar 3 rondas gana la partida.

Cada jugador elige una de tres facciones (Medieval, Futurista u Oscura),
que cambian el aspecto visual de torres, muros, unidades y base. Los dos
jugadores no pueden usar la misma faccion en una partida.

## Requisitos

- Python 3 (incluye Tkinter, que se usa para toda la interfaz)
- pygame (solo para el sonido)

Instalar pygame:

```
pip install pygame
```

Si pygame no esta instalado, el juego igual funciona, solo que sin sonido.

## Como ejecutar

```
python main.py
```

Orden de las pantallas al abrir:

1. Login del Jugador 1 (puede registrarse ahi mismo si no tiene cuenta).
2. El Jugador 1 elige su rol: Defensor o Atacante.
3. Login del Jugador 2 (debe ser una cuenta distinta a la del Jugador 1).
   Le toca automaticamente el rol contrario al del Jugador 1.
4. El Defensor elige su faccion entre las 3 disponibles.
5. El Atacante elige su faccion entre las 2 que quedaron.
6. Se abre el juego.

Desde la ventana de login estan los botones "Ranking" (top 5 de cada rol)
y "Ajustes" (volumen y pantalla completa).

## Como se juega

El juego es por turnos: en cada momento solo juega un jugador, y el
panel de la derecha indica claramente de quien es el turno (en dorado
el Defensor, en morado el Atacante).

**Turno del Defensor (fase de construccion):**
Solo el Defensor juega. El panel muestra sus controles. Presiona la
tecla de lo que quieres colocar y haz clic en el mapa:

| Tecla | Coloca        | Costo |
|-------|---------------|-------|
| 1     | Torre Basica  | 50    |
| 2     | Torre Pesada  | 120   |
| 3     | Torre Magica  | 100   |
| M     | Muro          | 30    |

Cuando termines, presiona "Terminar construccion".

**Turno del Atacante (fase de ataque):**
Solo el Atacante juega. Presiona la tecla de la unidad que quieres y
haz clic en una fila para que aparezca ahi:

| Tecla | Compra        | Costo |
|-------|---------------|-------|
| Q     | Soldado       | 40    |
| W     | Tanque        | 110   |
| E     | Unidad Rapida | 60    |

Debes comprar al menos una unidad. Cuando termines, presiona
"Empezar combate".


## Ajustes

La ventana de Ajustes (disponible desde el login y desde el juego) permite:

- Cambiar el volumen de los efectos de sonido.
- Cambiar el volumen de la musica de fondo.
- Activar o quitar la pantalla completa.

## Estructura del proyecto

```
main.py                  Archivo principal: login, roles, facciones y el juego
config.py                Constantes globales (rutas, dimensiones, economia, colores)
entidades.py             Clases de torres y unidades, con herencia
jugador.py               Clase Jugador y lectura/escritura de jugadores.json
facciones.py             Lee la informacion de las facciones desde el JSON
partida.py               Estado y logica de una partida: dinero, combate, rondas
tablero.py               Crea y dibuja el mapa y las unidades con imagenes
controles.py             Maneja las teclas para elegir que colocar
recursos.py              Carga de imagenes y sonidos, control de volumen y musica
widgets.py               Boton de imagen reutilizable para la interfaz
datos/                   Archivos JSON (jugadores, facciones)
assets/                  Imagenes y sonidos que usa el juego
  facciones/             Imagenes de cada faccion (base, torre, unidad, muro)
  mapa/                  Imagenes de fondo del mapa por faccion
  ui/                    Imagenes de los botones (en 3 tamanos)
  iconos/                Icono de la moneda
  sonidos/               Efectos de sonido y musica
interfaz/                Ventanas de Tkinter
  ventana_login.py       Registro e inicio de sesion
  ventana_seleccion.py   Eleccion de rol y de faccion
  ventana_ranking.py     Top 5 de defensores y de atacantes
  ventana_ajustes.py     Volumen y pantalla completa
```

## Creditos de los assets

Todas las imagenes y los efectos de sonido son de Kenney (www.kenney.nl),
con licencia Creative Commons CC0 (uso libre). Se usaron los paquetes
Tower Defense (Top-Down), Medieval RTS, Sci-Fi RTS, UI Pack, Impact Sounds,
Interface Sounds, RPG Audio y Sci-Fi Sounds. La musica de fondo fue
agregada aparte por los integrantes.
