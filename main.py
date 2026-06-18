'''
Archivo principal del proyecto Defensa y Asalto de Base.
Por ahora abre la ventana y dibuja el tablero del juego.
Falta conectar el login, la seleccion de faccion y el resto
del flujo de una partida.
'''

import tkinter as tk
import config
import tablero


def main():
    '''
    #E: no recibe parametros
    #S: crea la ventana principal, el canvas del tablero, y dibuja el mapa
    #R: no retorna nada
    '''
    ventana = tk.Tk()
    ventana.title(config.titulo_ventana)
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

    ventana.mainloop()


if __name__ == "__main__":
    main()
