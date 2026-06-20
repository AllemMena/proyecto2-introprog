#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import os
import tkinter as tk
import config

# pygame solo se usa para los sonidos. Si no esta instalado o falla,
# el juego sigue funcionando sin audio.
try:
    import pygame
    pygame.mixer.init()
    audio_disponible = True
except Exception:
    audio_disponible = False

# Aqui se guardan las imagenes ya cargadas para no leerlas del disco
# cada vez. La llave es la ruta del archivo.
_imagenes_guardadas = {}

# Aqui se guardan los sonidos ya cargados.
_sonidos_guardados = {}

# Ventana raiz unica de toda la aplicacion. Se crea una sola vez y se
# mantiene oculta. Todas las imagenes se asocian a esta raiz para que
# no se borren al cerrar las ventanas de cada pantalla.
_raiz = None

# Volumen actual (se puede cambiar desde la ventana de ajustes).
volumen_efectos = config.volumen_efectos
volumen_musica = config.volumen_musica


def obtener_raiz():
    '''
    #E: no recibe parametros
    #S: crea la ventana raiz unica la primera vez que se llama, y la
        deja oculta. Las siguientes veces devuelve la misma
    #R: retorna la ventana raiz (tk.Tk)
    '''
    global _raiz
    if _raiz is None:
        _raiz = tk.Tk()
        _raiz.withdraw()
    return _raiz


def cargar_imagen(ruta):
    '''
    #E: ruta (str) del archivo de imagen
    #S: carga la imagen como PhotoImage de Tkinter, asociada a la raiz
        unica. Si ya se cargo antes, devuelve la guardada
    #R: retorna el objeto PhotoImage, o None si el archivo no existe
    '''
    if ruta in _imagenes_guardadas:
        return _imagenes_guardadas[ruta]

    if not os.path.exists(ruta):
        return None

    imagen = tk.PhotoImage(file=ruta, master=obtener_raiz())
    _imagenes_guardadas[ruta] = imagen
    return imagen


def cargar_sonido(nombre):
    '''
    #E: nombre (str) del sonido, sin extension (ej "click")
    #S: carga el sonido .ogg desde la carpeta de sonidos
    #R: retorna el objeto Sound de pygame, o None si no hay audio
    '''
    if not audio_disponible:
        return None

    if nombre in _sonidos_guardados:
        return _sonidos_guardados[nombre]

    ruta = os.path.join(config.ruta_sonidos, nombre + ".ogg")
    if not os.path.exists(ruta):
        return None

    sonido = pygame.mixer.Sound(ruta)
    _sonidos_guardados[nombre] = sonido
    return sonido


def reproducir_sonido(nombre):
    '''
    #E: nombre (str) del sonido a reproducir
    #S: reproduce el efecto con el volumen actual de efectos
    #R: no retorna nada
    '''
    if not audio_disponible:
        return

    sonido = cargar_sonido(nombre)
    if sonido is not None:
        sonido.set_volume(volumen_efectos)
        sonido.play()


def reproducir_musica(nombre_archivo):
    '''
    #E: nombre_archivo (str) con extension (ej "musica_menu.mp3")
    #S: pone una musica de fondo en bucle con el volumen actual
    #R: no retorna nada
    '''
    if not audio_disponible:
        return

    ruta = os.path.join(config.ruta_sonidos, nombre_archivo)
    if not os.path.exists(ruta):
        return

    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen_musica)
        pygame.mixer.music.play(-1)
    except Exception:
        pass


def detener_musica():
    '''
    #E: no recibe parametros
    #S: detiene la musica de fondo que este sonando
    #R: no retorna nada
    '''
    if audio_disponible:
        pygame.mixer.music.stop()


def cambiar_volumen_efectos(valor):
    '''
    #E: valor (float) entre 0.0 y 1.0
    #S: actualiza el volumen de los efectos de sonido
    #R: no retorna nada
    '''
    global volumen_efectos
    volumen_efectos = valor


def cambiar_volumen_musica(valor):
    '''
    #E: valor (float) entre 0.0 y 1.0
    #S: actualiza el volumen de la musica de fondo, incluyendo la que
        este sonando en ese momento
    #R: no retorna nada
    '''
    global volumen_musica
    volumen_musica = valor
    if audio_disponible:
        pygame.mixer.music.set_volume(valor)
