#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import json
import config


def cargar_facciones():
    '''
    #E: no recibe parametros
    #S: lee el archivo de facciones
    #R: retorna el diccionario con los datos de las facciones disponibles
    '''
    archivo = open(config.archivo_facciones, "r")
    datos = json.load(archivo)
    archivo.close()
    return datos
