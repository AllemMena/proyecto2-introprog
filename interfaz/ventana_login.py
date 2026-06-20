'''
Archivo para manejar la ventana de registro e inicio de sesión.
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
    '''Revisa si el archivo JSON existe y lee los datos guardados.'''
    if os.path.exists(config.archivo_jugadores):
        with open(config.archivo_jugadores, "r") as archivo:
            #Si el archivo está vacío por error, json.load puede fallar, lo protegemos
            try:
                return json.load(archivo)
            except:
                return {}
    return {} #Si no existe, devuelve un diccionario vacío

def guardar_jugadores(datos):
    '''Guarda el diccionario de jugadores en el archivo JSON.'''
    with open(config.archivo_jugadores, "w") as archivo:
        json.dump(datos, archivo, indent=4)

def abrir_ventana():
    '''Crea y muestra la ventana de Tkinter con los botones y entradas.'''
    ventana = tk.Tk()
    ventana.title("Defensa y Asalto - Login")
    ventana.geometry("350x250")
    ventana.configure(bg="#0d0d12") # Usamos el color de fondo oscuro del tablero

    #Estas variables guardan lo que el jugador escriba en las cajitas de texto
    var_usuario = tk.StringVar()
    var_contrasena = tk.StringVar()

    # --- Funciones de los botones ---
    def registrarse():
        usuario = var_usuario.get()
        contrasena = var_contrasena.get()
        
        #Validamos que no dejen espacios vacíos
        if usuario == "" or contrasena == "":
            messagebox.showerror("Error", "¡No puedes dejar espacios vacíos!")
            return

        datos_jugadores = cargar_jugadores()
        
        #Revisamos que el usuario no exista ya en el JSON
        if usuario in datos_jugadores:
            messagebox.showerror("Error", "Ese nombre de usuario ya está en uso.")
        else:
            #Creamos el jugador nuevo usando la clase Jugador
            nuevo_jugador = Jugador(usuario, contrasena)
            #Lo guardamos en el diccionario general usando su método a_diccionario()
            datos_jugadores[usuario] = nuevo_jugador.a_diccionario()
            guardar_jugadores(datos_jugadores)
            messagebox.showinfo("Éxito", f"¡Jugador {usuario} registrado correctamente!")

    def iniciar_sesion():
        usuario = var_usuario.get()
        contrasena = var_contrasena.get()
        
        datos_jugadores = cargar_jugadores()
        
        #Buscamos el usuario en el JSON
        if usuario in datos_jugadores:
            #Comparamos la contraseña
            if datos_jugadores[usuario]["contrasena"] == contrasena:
                #Usamos la función que pidió Allen para cargar al jugador en memoria
                jugador_actual = crear_jugador_desde_diccionario(datos_jugadores[usuario])
                messagebox.showinfo("Éxito", f"¡Bienvenido de vuelta, {jugador_actual.usuario}!")
                
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
        else:
            messagebox.showerror("Error", "El usuario no existe, debes registrarte primero.")

    # --- Diseño visual de la ventana ---
    
    #Etiqueta y cajita para el Usuario
    tk.Label(ventana, text="Usuario:", bg="#0d0d12", fg="white", font=("Arial", 12)).pack(pady=(20, 5))
    tk.Entry(ventana, textvariable=var_usuario, font=("Arial", 12)).pack()

    #Etiqueta y cajita para la Contraseña (oculta con asteriscos)
    tk.Label(ventana, text="Contraseña:", bg="#0d0d12", fg="white", font=("Arial", 12)).pack(pady=(10, 5))
    tk.Entry(ventana, textvariable=var_contrasena, font=("Arial", 12), show="*").pack()

    #Botones
    tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion, bg="#2a5a7a", fg="white", font=("Arial", 10, "bold")).pack(pady=(20, 5))
    tk.Button(ventana, text="Registrarse", command=registrarse, bg="#5a4a32", fg="white", font=("Arial", 10)).pack()

    #Arrancamos la ventana
    ventana.mainloop()


if __name__ == "__main__":
    abrir_ventana()
