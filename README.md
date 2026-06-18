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

**Version 0**: estructura base del proyecto.

- [x] Estructura de carpetas
- [x] Clases base con herencia: `EntidadCombate`, `Torre`, `Unidad`
- [x] Subclases de torres: `TorreBasica`, `TorrePesada`, `TorreMagica`
- [x] Subclases de unidades: `Soldado`, `Tanque`, `UnidadRapida`
- [x] Clase `Jugador`
- [ ] Mapa en Tkinter (Canvas 10x10)
- [ ] Colocacion de torres y muros (fase de construccion)
- [ ] Compra y movimiento de unidades (fase de ataque)
- [ ] Fase de combate
- [ ] Sistema de rondas y condiciones de victoria
- [ ] Login y registro de jugadores
- [ ] Ranking (top 5 defensor / top 5 atacante)
- [ ] Seleccion de faccion
- [ ] Documentacion tecnica y manual de usuario

## Como ejecutar

```
python main.py
```

## Estructura del proyecto

```
main.py            Archivo principal
config.py           Constantes globales (rutas, dimensiones, economia)
entidades.py         Clases de torres y unidades, con herencia
jugador.py           Clase Jugador
datos/               Archivos JSON (jugadores, facciones)
assets/              Imagenes y sonidos
interfaz/            Ventanas de Tkinter (login, juego, ranking)
```
