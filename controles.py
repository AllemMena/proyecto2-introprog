'''
Maneja las teclas que el jugador presiona para elegir que va a colocar
en el mapa (que tipo de torre, unidad o muro queda seleccionado antes
de hacer clic en una casilla).
'''

# Guarda que esta seleccionado actualmente. Empieza en None porque
# al inicio de la partida no hay nada seleccionado todavia.
seleccion_actual = None

# Diccionario que relaciona cada tecla con el tipo que selecciona.
teclas_entidades = {
    "1": "basica",   # Torre Basica
    "2": "pesada",   # Torre Pesada
    "3": "magica",   # Torre Magica
    "q": "soldado",
    "w": "tanque",
    "e": "rapida",
    "m": "muro",
}


def procesar_tecla(tecla):
    '''
    #E: tecla (str), la tecla que el jugador presiono
    #S: si la tecla esta en el diccionario, actualiza la seleccion actual
    #R: retorna la seleccion actual (puede ser la nueva o la que ya estaba)
    '''
    global seleccion_actual

    tecla_minuscula = tecla.lower()

    if tecla_minuscula in teclas_entidades:
        seleccion_actual = teclas_entidades[tecla_minuscula]

    return seleccion_actual
