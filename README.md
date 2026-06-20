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

Dentro del juego, estas teclas seleccionan que se va a colocar:

| Tecla | Selecciona    |
|-------|---------------|
| 1     | Torre Basica  |
| 2     | Torre Pesada  |
| 3     | Torre Magica  |
| Q     | Soldado       |
| W     | Tanque        |
| E     | Unidad Rapida |
| M     | Muro          |

Fases de una ronda:

- **Construccion**: el Defensor selecciona una torre o un muro con el
  teclado y hace clic en el mapa para colocarlo. Cada cosa cuesta dinero.
- **Ataque**: con el boton "Pasar a ataque", el Atacante selecciona un
  tipo de unidad y hace clic en una fila para comprarla. La unidad aparece
  en el lado izquierdo.
- **Combate**: con "Iniciar combate" y luego "Siguiente turno", las torres
  disparan a las unidades en su alcance y las unidades avanzan o atacan lo
  que tengan en su camino (torre, muro o base).

Una ronda la gana el Defensor si elimina todas las unidades del Atacante,
o el Atacante si la vida de la base llega a cero. El primero en ganar 3
rondas gana la partida, y esa victoria se guarda en su cuenta para el
ranking.

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
  ui/                    Imagenes de los botones
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
