#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import tkinter as tk
from tkinter import messagebox
import os
import sys

ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_raiz)

import config
import recursos
from widgets import BotonImagen
from jugador import Jugador, crear_jugador_desde_diccionario, cargar_jugadores, guardar_jugadores
from interfaz.ventana_ranking import mostrar_ranking
from interfaz.ventana_ajustes import mostrar_ajustes


def abrir_ventana(subtitulo="Inicia sesion para jugar"):
    '''
    #E: subtitulo (str), texto pequeno bajo el titulo, util para
        indicar de que jugador es el turno de iniciar sesion
    #S: crea la ventana de login/registro sobre un canvas decorado,
        con el titulo del juego, campos de usuario y contrasena, y
        botones para iniciar sesion, registrarse, ver ranking y ajustes
    #R: retorna el objeto Jugador que inicio sesion, o None si se
        cerro la ventana sin iniciar sesion
    '''
    ventana = tk.Toplevel(recursos.obtener_raiz())
    ventana.title("Defensa y Asalto de Base")
    ancho, alto = 460, 620
    ventana.geometry(str(ancho) + "x" + str(alto))
    ventana.configure(bg=config.color_fondo)
    ventana.resizable(False, False)
    # Si el jugador cierra la ventana con la X, se trata como cancelar
    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)

    recursos.reproducir_musica("musica_menu.mp3")

    lienzo = tk.Canvas(ventana, width=ancho, height=alto, bg=config.color_fondo,
                       highlightthickness=0)
    lienzo.pack(fill="both", expand=True)

    # --- Decoracion de fondo: dos franjas suaves ---
    lienzo.create_rectangle(0, 0, ancho, 150, fill=config.color_panel, outline="")

    # --- Titulo del juego ---
    lienzo.create_text(ancho // 2, 58, text="DEFENSA Y ASALTO",
                       fill=config.color_dorado,
                       font=(config.fuente_titulo, 26, "bold"))
    lienzo.create_text(ancho // 2, 100, text="DE BASE", fill=config.color_morado,
                       font=(config.fuente_titulo, 22, "bold"))
    lienzo.create_text(ancho // 2, 175, text=subtitulo, fill=config.color_texto_suave,
                       font=(config.fuente_normal, 11))

    var_usuario = tk.StringVar()
    var_contrasena = tk.StringVar()
    jugador_que_entro = [None]

    # --- Campos de texto (Entry van encima del canvas) ---
    lienzo.create_text(95, 225, text="Usuario", fill=config.color_texto,
                       font=(config.fuente_normal, 11), anchor="w")
    entrada_usuario = tk.Entry(ventana, textvariable=var_usuario,
                               font=(config.fuente_normal, 12), bg=config.color_panel_claro,
                               fg=config.color_texto, insertbackground=config.color_texto,
                               relief="flat", justify="center")
    lienzo.create_window(ancho // 2, 255, window=entrada_usuario, width=300, height=34)

    lienzo.create_text(95, 300, text="Contrasena", fill=config.color_texto,
                       font=(config.fuente_normal, 11), anchor="w")
    entrada_contrasena = tk.Entry(ventana, textvariable=var_contrasena,
                                  font=(config.fuente_normal, 12), bg=config.color_panel_claro,
                                  fg=config.color_texto, insertbackground=config.color_texto,
                                  relief="flat", justify="center", show="*")
    lienzo.create_window(ancho // 2, 330, window=entrada_contrasena, width=300, height=34)

    # --- Acciones ---
    def registrarse():
        usuario = var_usuario.get()
        contrasena = var_contrasena.get()

        if usuario == "" or contrasena == "":
            recursos.reproducir_sonido("error")
            messagebox.showerror("Error", "No puedes dejar campos vacios.")
            return

        datos_jugadores = cargar_jugadores()

        if usuario in datos_jugadores:
            recursos.reproducir_sonido("error")
            messagebox.showerror("Error", "Ese nombre de usuario ya esta en uso.")
        else:
            nuevo_jugador = Jugador(usuario, contrasena)
            datos_jugadores[usuario] = nuevo_jugador.a_diccionario()
            guardar_jugadores(datos_jugadores)
            messagebox.showinfo("Exito", "Jugador " + usuario + " registrado.\nYa puedes iniciar sesion.")

    def iniciar_sesion():
        usuario = var_usuario.get()
        contrasena = var_contrasena.get()

        datos_jugadores = cargar_jugadores()

        if usuario not in datos_jugadores:
            recursos.reproducir_sonido("error")
            messagebox.showerror("Error", "El usuario no existe, debes registrarte primero.")
            return

        if datos_jugadores[usuario]["contrasena"] != contrasena:
            recursos.reproducir_sonido("error")
            messagebox.showerror("Error", "Contrasena incorrecta.")
            return

        jugador_que_entro[0] = crear_jugador_desde_diccionario(datos_jugadores[usuario])
        ventana.destroy()

    def ver_ranking():
        mostrar_ranking(ventana)

    def ver_ajustes():
        mostrar_ajustes(ventana)

    # --- Botones (imagenes sobre el canvas) ---
    BotonImagen(lienzo, ancho // 2, 400, "Iniciar sesion", iniciar_sesion,
                color="amarillo", tam_fuente=14)
    BotonImagen(lienzo, ancho // 2, 462, "Registrarse", registrarse, color="azul")
    BotonImagen(lienzo, ancho // 2 - 70, 530, "Ranking", ver_ranking,
                color="gris", ancho=130, tam_fuente=11)
    BotonImagen(lienzo, ancho // 2 + 70, 530, "Ajustes", ver_ajustes,
                color="gris", ancho=130, tam_fuente=11)

    ventana.wait_window()

    return jugador_que_entro[0]


if __name__ == "__main__":
    resultado = abrir_ventana()
    print("Jugador que inicio sesion:", resultado)
