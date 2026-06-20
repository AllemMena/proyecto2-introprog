#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import json
import os
import config


class Jugador:
    '''Representa a un jugador registrado en el sistema.'''

    def __init__(self, usuario, contrasena, victorias_defensor=0, victorias_atacante=0):
        '''
        #E: usuario (str), contrasena (str), victorias_defensor (int), victorias_atacante (int)
        #S: guarda los datos de cuenta del jugador
        #R: no retorna nada
        '''
        self.usuario = usuario
        self.contrasena = contrasena
        self.victorias_defensor = victorias_defensor
        self.victorias_atacante = victorias_atacante
        self.dinero = 0
        self.faccion = ""

    def sumar_victoria(self, rol):
        '''
        #E: rol (str), "defensor" o "atacante"
        #S: suma uno al contador de victorias que corresponda segun el rol
        #R: no retorna nada
        '''
        if rol == "defensor":
            self.victorias_defensor = self.victorias_defensor + 1
        elif rol == "atacante":
            self.victorias_atacante = self.victorias_atacante + 1

    def a_diccionario(self):
        '''
        #E: no recibe parametros
        #S: junta los datos del jugador en un diccionario para poder
            guardarlos despues en el archivo JSON
        #R: retorna un diccionario
        '''
        datos = {
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante,
        }
        return datos


def crear_jugador_desde_diccionario(datos):
    '''
    #E: datos (dict), un diccionario leido desde el archivo JSON
    #S: crea un objeto Jugador con la informacion de ese diccionario
    #R: retorna un objeto Jugador
    '''
    return Jugador(
        datos["usuario"],
        datos["contrasena"],
        datos["victorias_defensor"],
        datos["victorias_atacante"],
    )


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
