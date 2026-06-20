#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import config
import entidades
import tablero as tablero_mod


class Partida:
    '''Guarda todo lo que pasa durante una partida.'''

    def __init__(self):
        '''
        #E: no recibe parametros
        #S: prepara el tablero vacio, el dinero inicial de cada jugador,
            las listas de torres y unidades, la vida de la base, y deja
            la partida en la fase de construccion
        #R: no retorna nada
        '''
        self.tablero = tablero_mod.crear_tablero()
        self.dinero_defensor = config.dinero_inicial_defensor
        self.dinero_atacante = config.dinero_inicial_atacante
        self.vida_base = config.vida_base

        self.torres = []
        self.unidades = []
        self.vida_muros = {}

        self.ronda_actual = 1
        self.victorias_defensor = 0
        self.victorias_atacante = 0
        self.fase = "construccion"

    def reiniciar(self):
        '''
        #E: no recibe parametros
        #S: deja la partida como recien empezada: tablero vacio, dinero
            inicial, sin torres ni unidades, ronda 1 y marcador en cero
        #R: no retorna nada
        '''
        self.tablero = tablero_mod.crear_tablero()
        self.dinero_defensor = config.dinero_inicial_defensor
        self.dinero_atacante = config.dinero_inicial_atacante
        self.vida_base = config.vida_base
        self.torres = []
        self.unidades = []
        self.vida_muros = {}
        self.ronda_actual = 1
        self.victorias_defensor = 0
        self.victorias_atacante = 0
        self.fase = "construccion"

    # ========================================================
    # FASE DE CONSTRUCCION
    # ========================================================
    def colocar_torre(self, tipo, fila, columna):
        '''
        #E: tipo (str), fila (int), columna (int)
        #S: revisa que la casilla este vacia y que alcance el dinero,
            crea la torre, la coloca en el tablero y resta el costo
        #R: retorna True si se coloco, False si no se pudo
        '''
        if self.tablero[fila][columna] is not None:
            return False

        torre_nueva = entidades.crear_torre(tipo)

        if torre_nueva.costo > self.dinero_defensor:
            return False

        torre_nueva.colocar(fila, columna)
        self.tablero[fila][columna] = tipo
        self.torres.append(torre_nueva)
        self.dinero_defensor = self.dinero_defensor - torre_nueva.costo
        return True

    def colocar_muro(self, fila, columna):
        '''
        #E: fila (int), columna (int)
        #S: revisa que la casilla este vacia y que alcance el dinero,
            coloca el muro con su vida inicial y resta el costo
        #R: retorna True si se coloco, False si no se pudo
        '''
        if self.tablero[fila][columna] is not None:
            return False

        if config.costo_muro > self.dinero_defensor:
            return False

        self.tablero[fila][columna] = "muro"
        self.vida_muros[(fila, columna)] = config.vida_muro
        self.dinero_defensor = self.dinero_defensor - config.costo_muro
        return True

    # ========================================================
    # FASE DE ATAQUE
    # ========================================================
    def comprar_unidad(self, tipo, fila):
        '''
        #E: tipo (str), fila (int) donde va a aparecer la unidad
        #S: revisa que alcance el dinero, crea la unidad en la columna 0
            de esa fila y resta el costo
        #R: retorna True si se compro, False si no se pudo
        '''
        unidad_nueva = entidades.crear_unidad(tipo)

        if unidad_nueva.costo > self.dinero_atacante:
            return False

        unidad_nueva.colocar(fila, 0)
        self.unidades.append(unidad_nueva)
        self.dinero_atacante = self.dinero_atacante - unidad_nueva.costo
        return True

    # ========================================================
    # COMBATE
    # ========================================================
    def buscar_unidades_en_alcance(self, torre):
        '''
        #E: torre (Torre)
        #S: recorre las unidades con un for y junta las que estan vivas
            y dentro del alcance de la torre
        #R: retorna una lista (puede quedar vacia)
        '''
        encontradas = []
        for unidad in self.unidades:
            if unidad.esta_viva() and torre.en_alcance(unidad.fila, unidad.columna):
                encontradas.append(unidad)
        return encontradas

    def buscar_torre_en(self, fila, columna):
        '''
        #E: fila (int), columna (int)
        #S: recorre las torres con un for buscando una viva en esa posicion
        #R: retorna el objeto Torre si la encuentra, o None si no hay
        '''
        for torre in self.torres:
            if torre.esta_viva() and torre.fila == fila and torre.columna == columna:
                return torre
        return None

    def aplicar_dano_a_unidad(self, unidad, cantidad):
        '''
        #E: unidad (Unidad), cantidad (int) de dano a aplicar
        #S: si la unidad es un tanque con el escudo activo, reduce el
            dano a la mitad y apaga el escudo; si no, aplica el dano completo
        #R: no retorna nada
        '''
        if unidad.nombre == "Tanque" and unidad.escudo_activo:
            cantidad = cantidad // 2
            unidad.escudo_activo = False

        unidad.recibir_dano(cantidad)

    def avanzar_turno_combate(self):
        '''
        #E: no recibe parametros
        #S: en cada turno: las torres atacan a una unidad dentro de su
            alcance (usando su habilidad si ya esta lista), y cada
            unidad revisa la siguiente casilla de su camino para
            decidir si ataca una torre, un muro, dana la base, o avanza
        #R: no retorna nada
        '''
        # --- Ataque de las torres ---
        for torre in self.torres:
            if not torre.esta_viva():
                continue

            unidades_en_rango = self.buscar_unidades_en_alcance(torre)
            if len(unidades_en_rango) == 0:
                continue

            if torre.turnos_restantes == 0:
                if torre.nombre == "Torre Magica":
                    torre.usar_habilidad(unidades_en_rango)
                else:
                    torre.usar_habilidad(unidades_en_rango[0])
                torre.turnos_restantes = torre.turnos_habilidad
            else:
                self.aplicar_dano_a_unidad(unidades_en_rango[0], torre.dano)
                torre.turnos_restantes = torre.turnos_restantes - 1

            for unidad in unidades_en_rango:
                if not unidad.esta_viva():
                    self.dinero_defensor = self.dinero_defensor + config.dinero_por_unidad_eliminada

        # --- Movimiento o ataque de las unidades ---
        for unidad in self.unidades:
            if not unidad.esta_viva():
                continue

            if unidad.columna == config.columna_base:
                self.vida_base = self.vida_base - config.dano_unidad_a_base
                self.dinero_atacante = self.dinero_atacante + config.dinero_por_ataque_a_base
                continue

            if unidad.columna < config.columna_base:
                siguiente_columna = unidad.columna + 1
            else:
                siguiente_columna = unidad.columna - 1

            contenido = self.tablero[unidad.fila][siguiente_columna]

            if contenido in ("basica", "pesada", "magica"):
                self.atacar_torre(unidad, siguiente_columna)

            elif contenido == "muro":
                self.atacar_muro(unidad, siguiente_columna)

            else:
                if unidad.turnos_restantes == 0 and unidad.nombre != "Soldado":
                    unidad.usar_habilidad()
                    unidad.turnos_restantes = unidad.turnos_habilidad
                elif unidad.turnos_restantes > 0:
                    unidad.turnos_restantes = unidad.turnos_restantes - 1

                unidad.mover(config.columna_base)

    def atacar_torre(self, unidad, columna_torre):
        '''
        #E: unidad (Unidad) que ataca, columna_torre (int) donde esta la torre
        #S: la unidad le hace dano a la torre (o usa su habilidad si ya
            esta lista), y si la torre muere, la quita del tablero
        #R: no retorna nada
        '''
        torre_en_camino = self.buscar_torre_en(unidad.fila, columna_torre)
        if torre_en_camino is None:
            return

        if unidad.turnos_restantes == 0 and unidad.nombre == "Soldado":
            unidad.usar_habilidad(torre_en_camino)
            unidad.turnos_restantes = unidad.turnos_habilidad
        else:
            torre_en_camino.recibir_dano(unidad.dano)
            if unidad.turnos_restantes > 0:
                unidad.turnos_restantes = unidad.turnos_restantes - 1

        self.dinero_atacante = self.dinero_atacante + config.dinero_por_dano_a_torre

        if not torre_en_camino.esta_viva():
            self.tablero[unidad.fila][columna_torre] = None
            self.dinero_atacante = self.dinero_atacante + config.dinero_por_torre_destruida

    def atacar_muro(self, unidad, columna_muro):
        '''
        #E: unidad (Unidad) que ataca, columna_muro (int) donde esta el muro
        #S: resta la vida del muro en el diccionario vida_muros; si llega
            a cero, quita el muro del tablero y del diccionario
        #R: no retorna nada
        '''
        posicion = (unidad.fila, columna_muro)
        self.vida_muros[posicion] = self.vida_muros[posicion] - unidad.dano

        if self.vida_muros[posicion] <= 0:
            self.tablero[unidad.fila][columna_muro] = None
            del self.vida_muros[posicion]

    # ========================================================
    # RONDAS Y VICTORIA
    # ========================================================
    def verificar_ganador_ronda(self):
        '''
        #E: no recibe parametros
        #S: revisa las condiciones de victoria de la ronda actual.
            El dinero del atacante ya no importa en esta fase, porque
            las unidades solo se compran antes de iniciar el combate
        #R: retorna "atacante", "defensor", o None si la ronda sigue
        '''
        if self.vida_base <= 0:
            return "atacante"

        hay_unidades_vivas = False
        for unidad in self.unidades:
            if unidad.esta_viva():
                hay_unidades_vivas = True

        if not hay_unidades_vivas and len(self.unidades) > 0:
            return "defensor"

        return None

    def iniciar_nueva_ronda(self, ganador):
        '''
        #E: ganador (str), "defensor" o "atacante"
        #S: suma la victoria de ronda correspondiente y reinicia el
            tablero, el dinero, los muros y la vida de la base
        #R: no retorna nada
        '''
        if ganador == "defensor":
            self.victorias_defensor = self.victorias_defensor + 1
        elif ganador == "atacante":
            self.victorias_atacante = self.victorias_atacante + 1

        self.ronda_actual = self.ronda_actual + 1
        self.tablero = tablero_mod.crear_tablero()
        self.torres = []
        self.unidades = []
        self.vida_muros = {}
        self.dinero_defensor = config.dinero_inicial_defensor + config.dinero_extra_por_ronda
        self.dinero_atacante = config.dinero_inicial_atacante + config.dinero_extra_por_ronda
        self.vida_base = config.vida_base
        self.fase = "construccion"

    def hay_ganador_de_partida(self):
        '''
        #E: no recibe parametros
        #S: revisa si alguno de los dos jugadores ya llego a las
            rondas necesarias para ganar la partida completa
        #R: retorna "defensor", "atacante", o None si la partida sigue
        '''
        if self.victorias_defensor == config.rondas_para_ganar:
            return "defensor"
        elif self.victorias_atacante == config.rondas_para_ganar:
            return "atacante"
        return None
