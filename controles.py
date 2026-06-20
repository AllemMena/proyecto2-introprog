#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import entidades

# Guarda que esta seleccionado actualmente. Empieza en None porque
# al inicio de la partida no hay nada seleccionado todavia.
seleccion_actual = None

# Teclas del DEFENSOR (construye torres y muros).
teclas_defensor = {
    "1": "basica",
    "2": "pesada",
    "3": "magica",
    "m": "muro",
}

# Teclas del ATACANTE (compra unidades).
teclas_atacante = {
    "q": "soldado",
    "w": "tanque",
    "e": "rapida",
}


def procesar_tecla(tecla, fase):
    '''
    #E: tecla (str) que el jugador presiono, fase (str) actual de la
        partida ("construccion" o "ataque")
    #S: segun la fase, revisa solo las teclas del jugador que tiene el
        turno. Si la tecla le corresponde, actualiza la seleccion actual
    #R: retorna la seleccion actual
    '''
    global seleccion_actual

    tecla_minuscula = tecla.lower()

    if fase == "construccion" and tecla_minuscula in teclas_defensor:
        seleccion_actual = teclas_defensor[tecla_minuscula]
    elif fase == "ataque" and tecla_minuscula in teclas_atacante:
        seleccion_actual = teclas_atacante[tecla_minuscula]

    return seleccion_actual


def limpiar_seleccion():
    '''
    #E: no recibe parametros
    #S: deja la seleccion actual en None, util al cambiar de fase para
        que un jugador no herede lo que selecciono el otro
    #R: no retorna nada
    '''
    global seleccion_actual
    seleccion_actual = None


def lista_controles_defensor():
    '''
    #E: no recibe parametros
    #S: arma la lista de controles del defensor con su tecla, nombre y
        costo, para mostrarla en pantalla
    #R: retorna una lista de tuplas (tecla, nombre, costo)
    '''
    lista = []
    for tecla in ("1", "2", "3"):
        tipo = teclas_defensor[tecla]
        datos = entidades.datos_torres[tipo]
        lista.append((tecla.upper(), datos["nombre"], datos["costo"]))
    # El muro no esta en datos_torres, su costo esta en config
    import config
    lista.append(("M", "Muro", config.costo_muro))
    return lista


def lista_controles_atacante():
    '''
    #E: no recibe parametros
    #S: arma la lista de controles del atacante con su tecla, nombre y
        costo, para mostrarla en pantalla
    #R: retorna una lista de tuplas (tecla, nombre, costo)
    '''
    lista = []
    for tecla in ("q", "w", "e"):
        tipo = teclas_atacante[tecla]
        datos = entidades.datos_unidades[tipo]
        lista.append((tecla.upper(), datos["nombre"], datos["costo"]))
    return lista
