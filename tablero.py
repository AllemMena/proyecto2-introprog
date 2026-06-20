'''
Funciones para crear y dibujar el tablero del juego.
El tablero es una matriz (lista de listas) de filas x columnas.
Cada casilla guarda lo que hay ahi: None si esta vacia, o un
texto como "base", "muro", "torre" o "unidad".
'''

import config


def crear_tablero():
    '''
    #E: no recibe parametros
    #S: crea una matriz vacia del tamano definido en config y coloca
        la base en su posicion fija
    #R: retorna la matriz (lista de listas)
    '''
    tablero = []
    for fila in range(config.filas_mapa):
        fila_actual = []
        for columna in range(config.columnas_mapa):
            fila_actual.append(None)
        tablero.append(fila_actual)

    tablero[config.fila_base][config.columna_base] = "base"
    return tablero


def color_de_casilla(contenido):
    '''
    #E: contenido (str o None), lo que hay guardado en la casilla
    #S: decide que color usar segun el tipo de contenido
    #R: retorna un string con el color en formato hexadecimal
    '''
    if contenido == "base":
        return "#c9a24b"
    elif contenido == "muro":
        return "#5a4a32"
    elif contenido == "torre":
        return "#7a1a1a"
    elif contenido == "unidad":
        return "#2a5a7a"
    else:
        return "#1a1a24"


def dibujar_tablero(canvas, tablero):
    '''
    #E: canvas (tk.Canvas), tablero (matriz)
    #S: recorre la matriz con dos for (uno por fila y otro por columna)
        y dibuja un rectangulo por cada casilla, con su color segun
        el contenido
    #R: no retorna nada
    '''
    canvas.delete("all")

    for fila in range(config.filas_mapa):
        for columna in range(config.columnas_mapa):
            x1 = columna * config.tamano_casilla
            y1 = fila * config.tamano_casilla
            x2 = x1 + config.tamano_casilla
            y2 = y1 + config.tamano_casilla

            contenido = tablero[fila][columna]
            color = color_de_casilla(contenido)

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#0d0d12")


def dibujar_unidades(canvas, lista_unidades):
    '''
    #E: canvas (tk.Canvas), lista_unidades (list de Unidad)
    #S: recorre la lista con un for y dibuja un circulo por cada
        unidad que siga viva, en su posicion actual
    #R: no retorna nada
    '''
    for unidad in lista_unidades:
        if not unidad.esta_viva():
            continue

        x1 = unidad.columna * config.tamano_casilla + 10
        y1 = unidad.fila * config.tamano_casilla + 10
        x2 = x1 + config.tamano_casilla - 20
        y2 = y1 + config.tamano_casilla - 20

        canvas.create_oval(x1, y1, x2, y2, fill="#2a5a7a", outline="#5ab0d8")
