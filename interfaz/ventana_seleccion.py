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


def elegir_rol(nombre_jugador):
    '''
    #E: nombre_jugador (str)
    #S: muestra una ventana con dos botones grandes para que el
        jugador elija ser defensor o atacante
    #R: retorna "defensor" o "atacante"
    '''
    ventana = tk.Toplevel(recursos.obtener_raiz())
    ventana.title("Elegir rol")
    ancho, alto = 460, 420
    ventana.geometry(str(ancho) + "x" + str(alto))
    ventana.configure(bg=config.color_fondo)
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)

    lienzo = tk.Canvas(ventana, width=ancho, height=alto, bg=config.color_fondo,
                       highlightthickness=0)
    lienzo.pack(fill="both", expand=True)

    lienzo.create_rectangle(0, 0, ancho, 110, fill=config.color_panel, outline="")
    lienzo.create_text(ancho // 2, 50, text=nombre_jugador, fill=config.color_texto,
                       font=(config.fuente_normal, 16, "bold"))
    lienzo.create_text(ancho // 2, 85, text="elige tu rol para esta partida",
                       fill=config.color_texto_suave, font=(config.fuente_normal, 11))

    lienzo.create_text(ancho // 2, 160, text="El DEFENSOR construye torres y muros",
                       fill=config.color_dorado, font=(config.fuente_normal, 10))
    lienzo.create_text(ancho // 2, 250, text="El ATACANTE envia unidades a la base",
                       fill=config.color_morado, font=(config.fuente_normal, 10))

    rol_elegido = [None]

    def elegir(rol):
        rol_elegido[0] = rol
        ventana.destroy()

    BotonImagen(lienzo, ancho // 2, 195, "Defensor", lambda: elegir("defensor"),
                color="amarillo", ancho=260, tam_fuente=15)
    BotonImagen(lienzo, ancho // 2, 285, "Atacante", lambda: elegir("atacante"),
                color="azul", ancho=260, tam_fuente=15)

    ventana.wait_window()
    return rol_elegido[0]


def elegir_faccion(nombre_jugador, facciones_disponibles, datos_facciones):
    '''
    #E: nombre_jugador (str), facciones_disponibles (list de str con
        las facciones que todavia se pueden elegir), datos_facciones (dict)
    #S: muestra una tarjeta por cada faccion disponible, con la vista
        previa de sus imagenes (base, torre, unidad) y un boton para
        elegirla
    #R: retorna el nombre (str) de la faccion elegida
    '''
    ventana = tk.Toplevel(recursos.obtener_raiz())
    ventana.title("Elegir faccion")
    cantidad = len(facciones_disponibles)
    ancho = 300 * cantidad + 40
    alto = 460
    ventana.geometry(str(ancho) + "x" + str(alto))
    ventana.configure(bg=config.color_fondo)
    ventana.resizable(False, False)
    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)

    lienzo = tk.Canvas(ventana, width=ancho, height=alto, bg=config.color_fondo,
                       highlightthickness=0)
    lienzo.pack(fill="both", expand=True)

    lienzo.create_rectangle(0, 0, ancho, 90, fill=config.color_panel, outline="")
    lienzo.create_text(ancho // 2, 38, text=nombre_jugador, fill=config.color_texto,
                       font=(config.fuente_normal, 16, "bold"))
    lienzo.create_text(ancho // 2, 68, text="elige tu faccion",
                       fill=config.color_texto_suave, font=(config.fuente_normal, 11))

    faccion_elegida = [None]

    def elegir(faccion):
        faccion_elegida[0] = faccion
        ventana.destroy()

    # Una tarjeta por faccion
    for indice in range(cantidad):
        faccion = facciones_disponibles[indice]
        datos = datos_facciones[faccion]
        carpeta = datos["carpeta_assets"]
        acento = datos["color_acento"]

        centro_x = 20 + 300 * indice + 150
        tope = 120

        # Fondo de la tarjeta
        lienzo.create_rectangle(centro_x - 130, tope, centro_x + 130, tope + 290,
                                fill=config.color_panel, outline=acento, width=2)

        lienzo.create_text(centro_x, tope + 28, text=datos["nombre"], fill=acento,
                           font=(config.fuente_normal, 15, "bold"))

        # Vista previa: base, torre y unidad de la faccion
        piezas = ["base", "torre", "unidad"]
        etiquetas = ["Base", "Torre", "Unidad"]
        for j in range(3):
            ruta = os.path.join(config.ruta_facciones_img, carpeta, piezas[j] + ".png")
            imagen = recursos.cargar_imagen(ruta)
            px = centro_x - 80 + j * 80
            py = tope + 95
            if imagen is not None:
                lienzo.create_image(px, py, image=imagen)
            lienzo.create_text(px, py + 45, text=etiquetas[j], fill=config.color_texto_suave,
                               font=(config.fuente_normal, 9))

        BotonImagen(lienzo, centro_x, tope + 245, "Elegir",
                    lambda f=faccion: elegir(f), color="gris", ancho=200, tam_fuente=12)

    ventana.wait_window()
    return faccion_elegida[0]
