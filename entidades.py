#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2


# ============================================================
# DICCIONARIOS con los datos base de cada tipo de torre/unidad.
# Cada subclase busca aqui sus propios valores en vez de tenerlos
# escritos sueltos en el codigo.
# ============================================================
datos_torres = {
    "basica": {"nombre": "Torre Basica", "costo": 50, "vida": 80, "dano": 15,
               "alcance": 2, "turnos_habilidad": 3},
    "pesada": {"nombre": "Torre Pesada", "costo": 120, "vida": 200, "dano": 30,
               "alcance": 2, "turnos_habilidad": 4},
    "magica": {"nombre": "Torre Magica", "costo": 100, "vida": 60, "dano": 10,
               "alcance": 3, "turnos_habilidad": 5},
}

datos_unidades = {
    "soldado": {"nombre": "Soldado", "costo": 40, "vida": 60, "dano": 10,
                "velocidad": 1, "turnos_habilidad": 3},
    "tanque": {"nombre": "Tanque", "costo": 110, "vida": 220, "dano": 20,
               "velocidad": 1, "turnos_habilidad": 4},
    "rapida": {"nombre": "Unidad Rapida", "costo": 60, "vida": 50, "dano": 8,
               "velocidad": 3, "turnos_habilidad": 2},
}


# ============================================================
# CLASE PADRE
# ============================================================
class EntidadCombate:
    '''Clase base para las torres y las unidades.'''

    def __init__(self, nombre, costo, vida, dano, turnos_habilidad):
        '''
        #E: nombre (str), costo (int), vida (int), dano (int), turnos_habilidad (int)
        #S: guarda los datos basicos que comparten torres y unidades
        #R: no retorna nada
        '''
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida
        self.dano = dano
        self.turnos_habilidad = turnos_habilidad
        self.turnos_restantes = turnos_habilidad
        self.fila = 0
        self.columna = 0

    def recibir_dano(self, cantidad):
        '''
        #E: cantidad (int) de dano a recibir
        #S: resta la vida actual, sin dejarla bajar de cero
        #R: retorna True si la entidad murio, False si sigue viva
        '''
        self.vida_actual = self.vida_actual - cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0
        return self.vida_actual == 0

    def esta_viva(self):
        '''
        #E: no recibe parametros
        #S: revisa si la vida actual es mayor a cero
        #R: retorna un booleano
        '''
        return self.vida_actual > 0

    def colocar(self, fila, columna):
        '''
        #E: fila (int), columna (int)
        #S: guarda la posicion de la entidad dentro del mapa
        #R: no retorna nada
        '''
        self.fila = fila
        self.columna = columna

    def mostrar_informacion(self):
        '''
        #E: no recibe parametros
        #S: junta los datos principales de la entidad en un solo texto
        #R: retorna un string
        '''
        return self.nombre + " - Vida: " + str(self.vida_actual) + "/" + str(self.vida_maxima) + " - Dano: " + str(self.dano)


# ============================================================
# TORRES (heredan de EntidadCombate)
# ============================================================
class Torre(EntidadCombate):
    '''Clase para las torres defensivas. Agrega el alcance.'''

    def __init__(self, nombre, costo, vida, dano, turnos_habilidad, alcance):
        super().__init__(nombre, costo, vida, dano, turnos_habilidad)
        self.alcance = alcance

    def en_alcance(self, fila_objetivo, columna_objetivo):
        '''
        #E: fila_objetivo (int), columna_objetivo (int)
        #S: calcula que tan lejos esta el objetivo y lo compara con el alcance
        #R: retorna True si el objetivo esta dentro del alcance
        '''
        distancia = abs(self.fila - fila_objetivo) + abs(self.columna - columna_objetivo)
        return distancia <= self.alcance


class TorreBasica(Torre):
    '''Costo bajo, dano normal. Habilidad: disparo doble.'''

    def __init__(self):
        datos = datos_torres["basica"]
        super().__init__(datos["nombre"], datos["costo"], datos["vida"],
                          datos["dano"], datos["turnos_habilidad"], datos["alcance"])

    def usar_habilidad(self, objetivo):
        if objetivo.esta_viva():
            objetivo.recibir_dano(self.dano)
            objetivo.recibir_dano(self.dano)


class TorrePesada(Torre):
    '''Mucha vida y dano alto, costo elevado. Habilidad: golpe critico.'''

    def __init__(self):
        datos = datos_torres["pesada"]
        super().__init__(datos["nombre"], datos["costo"], datos["vida"],
                          datos["dano"], datos["turnos_habilidad"], datos["alcance"])

    def usar_habilidad(self, objetivo):
        objetivo.recibir_dano(self.dano * 2)


class TorreMagica(Torre):
    '''Dano bajo, pero habilidad fuerte: dano en area.'''

    def __init__(self):
        datos = datos_torres["magica"]
        super().__init__(datos["nombre"], datos["costo"], datos["vida"],
                          datos["dano"], datos["turnos_habilidad"], datos["alcance"])

    def usar_habilidad(self, lista_objetivos):
        '''
        #E: lista_objetivos (list de Unidad) las unidades dentro del alcance
        #S: recorre la lista con un for y le aplica dano a cada unidad viva
        #R: no retorna nada
        '''
        for unidad in lista_objetivos:
            if unidad.esta_viva():
                unidad.recibir_dano(self.dano)


# ============================================================
# UNIDADES (heredan de EntidadCombate)
# ============================================================
class Unidad(EntidadCombate):
    '''Clase para las unidades atacantes. Agrega la velocidad.'''

    def __init__(self, nombre, costo, vida, dano, turnos_habilidad, velocidad):
        super().__init__(nombre, costo, vida, dano, turnos_habilidad)
        self.velocidad = velocidad

    def mover(self, columna_base):
        '''
        #E: columna_base (int), columna donde esta la base
        #S: avanza la unidad lo que le permite su velocidad, sin pasarse
            de la columna de la base
        #R: no retorna nada
        '''
        distancia_restante = abs(self.columna - columna_base)
        pasos = min(self.velocidad, distancia_restante)

        if self.columna < columna_base:
            self.columna = self.columna + pasos
        else:
            self.columna = self.columna - pasos


class Soldado(Unidad):
    '''Bajo costo, estadisticas normales. Habilidad: ataque doble.'''

    def __init__(self):
        datos = datos_unidades["soldado"]
        super().__init__(datos["nombre"], datos["costo"], datos["vida"],
                          datos["dano"], datos["turnos_habilidad"], datos["velocidad"])

    def usar_habilidad(self, objetivo):
        if objetivo.esta_viva():
            objetivo.recibir_dano(self.dano)


class Tanque(Unidad):
    '''Mucha vida, movimiento lento. Habilidad: escudo temporal.'''

    def __init__(self):
        datos = datos_unidades["tanque"]
        super().__init__(datos["nombre"], datos["costo"], datos["vida"],
                          datos["dano"], datos["turnos_habilidad"], datos["velocidad"])
        self.escudo_activo = False

    def usar_habilidad(self, objetivo=None):
        # Activa el escudo. La reduccion de dano mientras este activo
        # se revisa despues, en la fase de combate (un simple if
        # antes de aplicar el dano).
        self.escudo_activo = True


class UnidadRapida(Unidad):
    '''Poco dano, se mueve mas rapido. Habilidad: aumento de velocidad.'''

    def __init__(self):
        datos = datos_unidades["rapida"]
        super().__init__(datos["nombre"], datos["costo"], datos["vida"],
                          datos["dano"], datos["turnos_habilidad"], datos["velocidad"])

    def usar_habilidad(self, objetivo=None):
        self.velocidad = self.velocidad + 2


# ============================================================
# FUNCIONES PARA CREAR TORRES Y UNIDADES SEGUN EL TIPO
# ============================================================
def crear_torre(tipo):
    '''
    #E: tipo (str), puede ser "basica", "pesada" o "magica"
    #S: revisa el tipo recibido y crea la torre que corresponda
    #R: retorna un objeto Torre (de la subclase que corresponda)
    '''
    if tipo == "basica":
        return TorreBasica()
    elif tipo == "pesada":
        return TorrePesada()
    elif tipo == "magica":
        return TorreMagica()


def crear_unidad(tipo):
    '''
    #E: tipo (str), puede ser "soldado", "tanque" o "rapida"
    #S: revisa el tipo recibido y crea la unidad que corresponda
    #R: retorna un objeto Unidad (de la subclase que corresponda)
    '''
    if tipo == "soldado":
        return Soldado()
    elif tipo == "tanque":
        return Tanque()
    elif tipo == "rapida":
        return UnidadRapida()
