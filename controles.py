'''
Archivo para manejar las teclas que presionan los jugadores.
'''

#Creamos una variable "vacía". 
#Imagina que es la mano del jugador: al inicio de la partida no tiene nada agarrado.
seleccion_actual = None

#Creamos el diccionario de teclas
teclas_entidades = {
    "1": "basica",   # Tecla 1 selecciona Torre Básica
    "2": "pesada",   # Tecla 2 selecciona Torre Pesada
    "3": "magica",   # Tecla 3 selecciona Torre Mágica
    "q": "soldado",  # Tecla Q selecciona Soldado
    "w": "tanque",   # Tecla W selecciona Tanque
    "e": "rapida",   # Tecla E selecciona Unidad Rápida
    "m": "muro"      # Tecla M selecciona el Muro 
}


def procesar_tecla(tecla):
    '''
    #E: tecla (str), la letra o número que el jugador presionó en su teclado.
    #S: revisa si esa tecla existe en nuestro diccionario y actualiza la selección.
    #R: retorna el texto de lo que seleccionaste (ej: "basica"), o None si tocaste otra tecla.
    '''
    global seleccion_actual #Le decimos a Python que vamos a modificar la "mano" del jugador

    #Convertimos la tecla a minúscula por si el jugador tenía las mayúsculas encendidas sin querer
    tecla_minuscula = tecla.lower()

    #Le preguntamos a Python: "¿La tecla que tocó el jugador está en nuestro diccionario?"
    if tecla_minuscula in teclas_entidades:
        #Si sí está, le ponemos a la "mano" del jugador el nombre de la torre o unidad
        seleccion_actual = teclas_entidades[tecla_minuscula]
        print(f"Has seleccionado: {seleccion_actual}") #Esto imprime un mensajito en la consola para confirmar
    
    return seleccion_actual
