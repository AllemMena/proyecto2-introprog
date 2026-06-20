#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import os
import config
import recursos


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


def imagen_de_faccion(carpeta, nombre):
    '''
    #E: carpeta (str) de la faccion (ej "medieval"), nombre (str) del
        archivo sin extension (ej "torre_basica")
    #S: arma la ruta de la imagen de esa pieza y la carga
    #R: retorna el PhotoImage, o None si no existe
    '''
    ruta = os.path.join(config.ruta_facciones_img, carpeta, nombre + ".png")
    return recursos.cargar_imagen(ruta)


def centro_de_casilla(fila, columna):
    '''
    #E: fila (int), columna (int)
    #S: calcula las coordenadas x, y del centro de esa casilla en el canvas
    #R: retorna una tupla (x, y)
    '''
    x = columna * config.tamano_casilla + config.tamano_casilla // 2
    y = fila * config.tamano_casilla + config.tamano_casilla // 2
    return x, y


def dibujar_fondo(canvas, faccion_defensor, datos_facciones):
    '''
    #E: canvas (tk.Canvas), faccion_defensor (str), datos_facciones (dict)
    #S: dibuja la imagen de fondo del mapa de la faccion del defensor,
        cubriendo todo el canvas; si no hay imagen, usa un color liso
    #R: no retorna nada
    '''
    nombre_fondo = datos_facciones[faccion_defensor]["fondo_mapa"]
    ruta_fondo = os.path.join(config.ruta_mapa_img, nombre_fondo)
    fondo = recursos.cargar_imagen(ruta_fondo)

    if fondo is not None:
        canvas.create_image(0, 0, image=fondo, anchor="nw")
    else:
        ancho = config.columnas_mapa * config.tamano_casilla
        alto = config.filas_mapa * config.tamano_casilla
        canvas.create_rectangle(0, 0, ancho, alto, fill=config.color_canvas, outline="")


def dibujar_lineas(canvas):
    '''
    #E: canvas (tk.Canvas)
    #S: dibuja las lineas de la cuadricula encima del fondo, para que
        se note la separacion de casillas
    #R: no retorna nada
    '''
    ancho = config.columnas_mapa * config.tamano_casilla
    alto = config.filas_mapa * config.tamano_casilla

    for i in range(config.columnas_mapa + 1):
        x = i * config.tamano_casilla
        canvas.create_line(x, 0, x, alto, fill="#000000", stipple="gray25")

    for i in range(config.filas_mapa + 1):
        y = i * config.tamano_casilla
        canvas.create_line(0, y, ancho, y, fill="#000000", stipple="gray25")


def nombre_archivo_pieza(contenido):
    '''
    #E: contenido (str) lo que hay en una casilla del tablero: "base",
        "muro", "basica", "pesada" o "magica"
    #S: traduce ese contenido al nombre de archivo de imagen que le
        corresponde dentro de la carpeta de la faccion
    #R: retorna el nombre de archivo (str), sin extension
    '''
    if contenido == "base":
        return "base"
    elif contenido == "muro":
        return "muro"
    elif contenido in ("basica", "pesada", "magica"):
        return "torre_" + contenido
    return contenido


def dibujar_tablero(canvas, tablero, faccion_defensor, datos_facciones):
    '''
    #E: canvas (tk.Canvas), tablero (matriz), faccion_defensor (str),
        datos_facciones (dict)
    #S: dibuja el fondo, la cuadricula, y encima la imagen que
        corresponda a cada casilla (base, torre segun su tipo, o muro)
        usando las imagenes de la faccion del defensor
    #R: no retorna nada
    '''
    canvas.delete("all")

    dibujar_fondo(canvas, faccion_defensor, datos_facciones)
    dibujar_lineas(canvas)

    carpeta = datos_facciones[faccion_defensor]["carpeta_assets"]

    for fila in range(config.filas_mapa):
        for columna in range(config.columnas_mapa):
            contenido = tablero[fila][columna]
            if contenido is None:
                continue

            imagen = imagen_de_faccion(carpeta, nombre_archivo_pieza(contenido))
            x, y = centro_de_casilla(fila, columna)

            if imagen is not None:
                canvas.create_image(x, y, image=imagen)
            else:
                # respaldo por si falta la imagen: un cuadro de color
                mitad = config.tamano_casilla // 2 - 6
                canvas.create_rectangle(x - mitad, y - mitad, x + mitad, y + mitad,
                                        fill=config.color_dorado, outline="")


def nombre_archivo_unidad(unidad):
    '''
    #E: unidad (Unidad)
    #S: traduce el nombre de la unidad al archivo de imagen que le
        corresponde dentro de la carpeta de la faccion
    #R: retorna el nombre de archivo (str), sin extension
    '''
    mapa_nombres = {
        "Soldado": "unidad_soldado",
        "Tanque": "unidad_tanque",
        "Unidad Rapida": "unidad_rapida",
    }
    return mapa_nombres.get(unidad.nombre, "unidad_soldado")


def dibujar_unidades(canvas, lista_unidades, faccion_atacante, datos_facciones):
    '''
    #E: canvas (tk.Canvas), lista_unidades (list de Unidad),
        faccion_atacante (str), datos_facciones (dict)
    #S: recorre la lista con un for y dibuja la imagen que le
        corresponde a cada tipo de unidad viva, con la faccion del atacante
    #R: no retorna nada
    '''
    carpeta = datos_facciones[faccion_atacante]["carpeta_assets"]

    for unidad in lista_unidades:
        if not unidad.esta_viva():
            continue

        imagen = imagen_de_faccion(carpeta, nombre_archivo_unidad(unidad))
        x, y = centro_de_casilla(unidad.fila, unidad.columna)

        if imagen is not None:
            canvas.create_image(x, y, image=imagen)
        else:
            radio = config.tamano_casilla // 2 - 12
            canvas.create_oval(x - radio, y - radio, x + radio, y + radio,
                               fill=config.color_morado, outline="white")


def dibujar_resaltado_fila(canvas, fila, color):
    '''
    #E: canvas (tk.Canvas), fila (int) a resaltar, color (str)
    #S: dibuja un marco semi-transparente sobre toda la fila, usado en
        la fase de ataque para mostrar donde va a aparecer la unidad
    #R: no retorna nada
    '''
    ancho = config.columnas_mapa * config.tamano_casilla
    y_arriba = fila * config.tamano_casilla
    y_abajo = y_arriba + config.tamano_casilla

    canvas.create_rectangle(0, y_arriba, ancho, y_abajo, fill="", outline=color,
                            width=3, tags="vista_previa")


def dibujar_resaltado_casilla(canvas, fila, columna, color, valido):
    '''
    #E: canvas (tk.Canvas), fila (int), columna (int), color (str),
        valido (bool) si la casilla esta libre o no
    #S: dibuja un marco sobre la casilla bajo el cursor, en el color
        de la faccion si esta libre, o en rojo si ya esta ocupada
    #R: no retorna nada
    '''
    x = columna * config.tamano_casilla
    y = fila * config.tamano_casilla
    tamano = config.tamano_casilla

    color_marco = color if valido else "#d65a5a"
    canvas.create_rectangle(x + 2, y + 2, x + tamano - 2, y + tamano - 2,
                            fill="", outline=color_marco, width=3, tags="vista_previa")


def dibujar_vista_previa_pieza(canvas, fila, columna, carpeta, nombre_archivo, valido):
    '''
    #E: canvas (tk.Canvas), fila (int), columna (int), carpeta (str) de
        la faccion, nombre_archivo (str) el archivo exacto a mostrar
        (ej "torre_basica", "muro", "unidad_tanque"), valido (bool) si
        se puede colocar ahi
    #S: dibuja la imagen de la pieza seleccionada centrada en la
        casilla bajo el cursor
    #R: no retorna nada
    '''
    imagen = imagen_de_faccion(carpeta, nombre_archivo)
    x, y = centro_de_casilla(fila, columna)

    if imagen is not None:
        canvas.create_image(x, y, image=imagen, tags="vista_previa")
    else:
        radio = config.tamano_casilla // 2 - 10
        relleno = config.color_dorado if valido else "#d65a5a"
        canvas.create_oval(x - radio, y - radio, x + radio, y + radio,
                           fill=relleno, outline="white", tags="vista_previa")
