#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import tkinter as tk
import os
import sys

ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_raiz)

import config
import recursos
from widgets import BotonImagen
from jugador import cargar_jugadores


def obtener_top(datos_jugadores, campo_victorias):
    '''
    #E: datos_jugadores (dict), campo_victorias (str): "victorias_defensor"
        o "victorias_atacante"
    #S: junta a todos los jugadores con ese tipo de victorias y los
        ordena de mayor a menor con un ordenamiento por seleccion
    #R: retorna una lista de listas [usuario, victorias], maximo 5
    '''
    lista_jugadores = []
    for usuario in datos_jugadores:
        victorias = datos_jugadores[usuario][campo_victorias]
        lista_jugadores.append([usuario, victorias])

    cantidad = len(lista_jugadores)
    for i in range(cantidad):
        indice_mayor = i
        for j in range(i + 1, cantidad):
            if lista_jugadores[j][1] > lista_jugadores[indice_mayor][1]:
                indice_mayor = j
        lista_jugadores[i], lista_jugadores[indice_mayor] = lista_jugadores[indice_mayor], lista_jugadores[i]

    return lista_jugadores[:5]


def dibujar_columna(lienzo, x, titulo, color, lista_top):
    '''
    #E: lienzo (tk.Canvas), x (int) centro de la columna, titulo (str),
        color (str) del titulo, lista_top (list de [usuario, victorias])
    #S: dibuja el titulo de la columna y debajo cada jugador con su
        posicion y cantidad de victorias
    #R: no retorna nada
    '''
    lienzo.create_text(x, 110, text=titulo, fill=color,
                       font=(config.fuente_normal, 13, "bold"))

    if len(lista_top) == 0:
        lienzo.create_text(x, 160, text="(sin datos todavia)", fill=config.color_texto_suave,
                           font=(config.fuente_normal, 10))
        return

    posicion = 1
    for jugador in lista_top:
        y = 110 + posicion * 40
        texto = str(posicion) + ".  " + jugador[0] + "  -  " + str(jugador[1])
        lienzo.create_text(x, y, text=texto, fill=config.color_texto,
                           font=(config.fuente_normal, 11))
        posicion = posicion + 1


def mostrar_ranking(ventana_padre):
    '''
    #E: ventana_padre (tk.Tk o tk.Toplevel), la ventana desde donde se abre
    #S: abre una ventana con el top 5 de defensores y el top 5 de
        atacantes, en dos columnas
    #R: no retorna nada
    '''
    datos_jugadores = cargar_jugadores()
    top_defensor = obtener_top(datos_jugadores, "victorias_defensor")
    top_atacante = obtener_top(datos_jugadores, "victorias_atacante")

    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Ranking de jugadores")
    ancho, alto = 520, 420
    ventana.geometry(str(ancho) + "x" + str(alto))
    ventana.configure(bg=config.color_fondo)
    ventana.resizable(False, False)

    lienzo = tk.Canvas(ventana, width=ancho, height=alto, bg=config.color_fondo,
                       highlightthickness=0)
    lienzo.pack(fill="both", expand=True)

    lienzo.create_rectangle(0, 0, ancho, 70, fill=config.color_panel, outline="")
    lienzo.create_text(ancho // 2, 38, text="RANKING DE JUGADORES", fill=config.color_texto,
                       font=(config.fuente_normal, 15, "bold"))

    dibujar_columna(lienzo, ancho // 4, "Top 5 Defensor", config.color_dorado, top_defensor)
    dibujar_columna(lienzo, 3 * ancho // 4, "Top 5 Atacante", config.color_morado, top_atacante)

    BotonImagen(lienzo, ancho // 2, 380, "Cerrar", ventana.destroy,
                color="gris", ancho=200, tam_fuente=12)


if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.withdraw()
    mostrar_ranking(raiz)
    raiz.mainloop()
