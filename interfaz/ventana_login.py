'''
Ventana de registro e inicio de sesion. Se muestra antes de entrar
al juego. Los jugadores se guardan en datos/jugadores.json como un
diccionario, usando el nombre de usuario como llave.
'''
import tkinter as tk
from tkinter import messagebox
import json
import os
import sys

ruta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_raiz)

import config
from jugador import Jugador, crear_jugador_desde_diccionario


def cargar_jugadores():
    '''
    #E: no recibe parametros
    #S: revisa si el archivo de jugadores existe y lo lee. Si el archivo
        esta vacio o dañado, json.load fallaria, por eso se protege con
        try/except
    #R: retorna el diccionario de jugadores (vacio si el archivo no
        existe o no se pudo leer)
    '''
    if os.path.exists(config.archivo_jugadores):
        archivo = open(config.archivo_jugadores, "r")
        try:
            datos = json.load(archivo)
        except json.JSONDecodeError:
            datos = {}
        archivo.close()
        return datos

    return {}


def guardar_jugadores(datos):
    '''
    #E: datos (dict) con todos los jugadores registrados
    #S: escribe ese diccionario completo en el archivo JSON
    #R: no retorna nada
    '''
    archivo = open(config.archivo_jugadores, "w")
    json.dump(datos, archivo, indent=4)
    archivo.close()


def abrir_ventana():
    '''
    #E: no recibe parametros
    #S: crea la ventana de login/registro y la mantiene abierta hasta
        que el jugador inicie sesion correctamente o la cierre
    #R: retorna el objeto Jugador que inicio sesion, o None si cerro
        la ventana sin iniciar sesion
    '''
    ventana = tk.Tk()
    ventana.title("Defensa y Asalto de Base - Login")
    ventana.geometry("350x250")
    ventana.configure(bg="#0d0d12")

    var_usuario = tk.StringVar()
    var_contrasena = tk.StringVar()

    # Aqui se guarda el jugador que logra iniciar sesion, para que
    # abrir_ventana() lo pueda devolver despues de cerrar la ventana.
    jugador_que_entro = [None]

    def registrarse():
        usuario = var_usuario.get()
        contrasena = var_contrasena.get()

        if usuario == "" or contrasena == "":
            messagebox.showerror("Error", "No puedes dejar campos vacios.")
            return

        datos_jugadores = cargar_jugadores()

        if usuario in datos_jugadores:
            messagebox.showerror("Error", "Ese nombre de usuario ya esta en uso.")
        else:
            nuevo_jugador = Jugador(usuario, contrasena)
            datos_jugadores[usuario] = nuevo_jugador.a_diccionario()
            guardar_jugadores(datos_jugadores)
            messagebox.showinfo("Exito", f"Jugador {usuario} registrado correctamente. Ya puedes iniciar sesion.")

    def iniciar_sesion():
        usuario = var_usuario.get()
        contrasena = var_contrasena.get()

        datos_jugadores = cargar_jugadores()

        if usuario not in datos_jugadores:
            messagebox.showerror("Error", "El usuario no existe, debes registrarte primero.")
            return

        if datos_jugadores[usuario]["contrasena"] != contrasena:
            messagebox.showerror("Error", "Contrasena incorrecta.")
            return

        jugador_que_entro[0] = crear_jugador_desde_diccionario(datos_jugadores[usuario])
        ventana.destroy()

    tk.Label(ventana, text="Usuario:", bg="#0d0d12", fg="white", font=("Arial", 12)).pack(pady=(20, 5))
    tk.Entry(ventana, textvariable=var_usuario, font=("Arial", 12)).pack()

    tk.Label(ventana, text="Contrasena:", bg="#0d0d12", fg="white", font=("Arial", 12)).pack(pady=(10, 5))
    tk.Entry(ventana, textvariable=var_contrasena, font=("Arial", 12), show="*").pack()

    tk.Button(ventana, text="Iniciar Sesion", command=iniciar_sesion, bg="#2a5a7a", fg="white", font=("Arial", 10, "bold")).pack(pady=(20, 5))
    tk.Button(ventana, text="Registrarse", command=registrarse, bg="#5a4a32", fg="white", font=("Arial", 10)).pack()

    ventana.mainloop()

    return jugador_que_entro[0]


if __name__ == "__main__":
    jugador_resultado = abrir_ventana()
    print("Jugador que inicio sesion:", jugador_resultado)
