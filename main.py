'''
Archivo principal del proyecto Defensa y Asalto de Base.
Primero pide login/registro, y solo si alguien inicia sesion
correctamente se abre la ventana del juego con el tablero.
Falta conectar la seleccion de faccion y el resto del flujo
de una partida.
'''

import tkinter as tk
import config
import tablero
import controles
from interfaz.ventana_login import abrir_ventana


def main():
    '''
    #E: no recibe parametros
    #S: muestra el login, y si alguien entra, abre la ventana del
        juego con el canvas del tablero y las teclas activas
    #R: no retorna nada
    '''
    jugador_actual = abrir_ventana()

    if jugador_actual is None:
        return

    ventana = tk.Tk()
    ventana.title(config.titulo_ventana + " - " + jugador_actual.usuario)
    ventana.geometry(f"{config.ancho_ventana}x{config.alto_ventana}")
    ventana.configure(bg="#0d0d12")

    ancho_tablero = config.columnas_mapa * config.tamano_casilla
    alto_tablero = config.filas_mapa * config.tamano_casilla

    canvas = tk.Canvas(
        ventana,
        width=ancho_tablero,
        height=alto_tablero,
        bg="#1a1a24",
        highlightthickness=0,
    )
    canvas.pack(side="left", padx=20, pady=20)

    matriz_tablero = tablero.crear_tablero()
    tablero.dibujar_tablero(canvas, matriz_tablero)

    def tecla_presionada(evento):
        controles.procesar_tecla(evento.char)

    ventana.bind("<Key>", tecla_presionada)

    ventana.mainloop()


if __name__ == "__main__":
    main()
