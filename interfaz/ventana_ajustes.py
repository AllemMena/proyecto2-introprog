#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import tkinter as tk
import os
import sys

ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_raiz)

import config
import recursos


def mostrar_ajustes(ventana_padre):
    '''
    #E: ventana_padre (tk.Tk o tk.Toplevel), la ventana desde donde se abre
    #S: abre una ventana de ajustes con dos barras de volumen (efectos
        y musica) y un boton para activar o quitar la pantalla completa
        de la ventana padre
    #R: no retorna nada
    '''
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Ajustes")
    ventana.geometry("420x360")
    ventana.configure(bg=config.color_fondo)
    ventana.resizable(False, False)

    tk.Label(ventana, text="AJUSTES", bg=config.color_fondo, fg=config.color_texto,
             font=(config.fuente_normal, 15, "bold")).pack(pady=(24, 20))

    # --- Volumen de efectos ---
    tk.Label(ventana, text="Volumen de efectos", bg=config.color_fondo,
             fg=config.color_dorado, font=(config.fuente_normal, 11)).pack(pady=(6, 0))

    def cambiar_efectos(valor):
        recursos.cambiar_volumen_efectos(int(valor) / 100.0)

    barra_efectos = tk.Scale(ventana, from_=0, to=100, orient="horizontal",
                             command=cambiar_efectos, length=300,
                             bg=config.color_panel, fg=config.color_texto,
                             troughcolor=config.color_panel_claro, highlightthickness=0,
                             relief="flat")
    barra_efectos.set(int(recursos.volumen_efectos * 100))
    barra_efectos.pack(pady=(0, 10))

    # --- Volumen de musica ---
    tk.Label(ventana, text="Volumen de musica", bg=config.color_fondo,
             fg=config.color_morado, font=(config.fuente_normal, 11)).pack(pady=(6, 0))

    def cambiar_musica(valor):
        recursos.cambiar_volumen_musica(int(valor) / 100.0)

    barra_musica = tk.Scale(ventana, from_=0, to=100, orient="horizontal",
                            command=cambiar_musica, length=300,
                            bg=config.color_panel, fg=config.color_texto,
                            troughcolor=config.color_panel_claro, highlightthickness=0,
                            relief="flat")
    barra_musica.set(int(recursos.volumen_musica * 100))
    barra_musica.pack(pady=(0, 16))

    # --- Pantalla completa ---
    def alternar_pantalla_completa():
        recursos.reproducir_sonido("click")
        estado_actual = ventana_padre.attributes("-fullscreen")
        ventana_padre.attributes("-fullscreen", not estado_actual)

    tk.Button(ventana, text="Activar / quitar pantalla completa",
              command=alternar_pantalla_completa, bg=config.color_panel_claro,
              fg=config.color_texto, font=(config.fuente_normal, 10), relief="flat",
              cursor="hand2").pack(pady=4, padx=40, fill="x", ipady=6)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy,
              bg=config.color_panel, fg=config.color_texto,
              font=(config.fuente_normal, 10), relief="flat",
              cursor="hand2").pack(pady=(10, 0), padx=40, fill="x", ipady=6)
