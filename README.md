# Defensa y Asalto de Base

Proyecto del curso Introduccion a la Programacion (Modalidad Live Learning),
Tecnologico de Costa Rica.

## Integrantes

- Allem Alejandro Mena Ruiz
- Joel Alpizar Ramirez

## Descripcion

Juego de estrategia para dos jugadores. Un jugador es el defensor y debe
construir una base con muros y torres defensivas; el otro jugador es el
atacante y debe destruir la base central usando distintas unidades.
El juego se juega por rondas y el primero en ganar 3 rondas gana la partida.

## Estado actual

- [x] Estructura de carpetas
- [x] Clases base con herencia: `EntidadCombate`, `Torre`, `Unidad`
- [x] Subclases de torres: `TorreBasica`, `TorrePesada`, `TorreMagica`
- [x] Subclases de unidades: `Soldado`, `Tanque`, `UnidadRapida`
- [x] Clase `Jugador`
- [x] Mapa en Tkinter (Canvas 10x10)
- [x] Login y registro de jugadores (guardado en JSON)
- [x] Controles de teclado para elegir que colocar (torres, unidades, muro)
- [ ] Colocacion de torres y muros (fase de construccion)
- [ ] Compra y movimiento de unidades (fase de ataque)
- [ ] Fase de combate
- [ ] Sistema de rondas y condiciones de victoria
- [ ] Ranking (top 5 defensor / top 5 atacante)
- [ ] Seleccion de faccion
- [ ] Documentacion tecnica y manual de usuario

## Como ejecutar

```
python main.py
```

Al abrir, primero aparece la ventana de login. Si no tienes cuenta,
te registras ahi mismo (usuario y contrasena). Despues de iniciar
sesion se abre la ventana del juego con el tablero.

Dentro del juego, estas teclas seleccionan que se va a colocar
(todavia no se puede colocar en el mapa, eso sigue en desarrollo):

| Tecla | Selecciona |
|-------|------------|
| 1     | Torre Basica |
| 2     | Torre Pesada |
| 3     | Torre Magica |
| Q     | Soldado |
| W     | Tanque |
| E     | Unidad Rapida |
| M     | Muro |

## Estructura del proyecto

```
main.py              Archivo principal: login y arranque del juego
config.py             Constantes globales (rutas, dimensiones, economia)
entidades.py           Clases de torres y unidades, con herencia
jugador.py             Clase Jugador
tablero.py             Crea y dibuja la matriz del mapa (Canvas)
controles.py           Maneja las teclas para elegir que colocar
datos/                 Archivos JSON (jugadores, facciones)
assets/                Imagenes y sonidos
interfaz/               Ventanas de Tkinter (login)
```
