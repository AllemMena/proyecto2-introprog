'''
Clase Jugador: representa a un usuario registrado, con su
informacion de cuenta y su historial de victorias.
'''


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
