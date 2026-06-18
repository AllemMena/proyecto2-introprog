'''
Constantes globales del proyecto Defensa y Asalto de Base.
Aqui se centralizan rutas de archivos, dimensiones de ventana
y valores fijos de la economia del juego.
'''

import os


# ============================================================
# RUTAS
# ============================================================
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_assets = os.path.join(ruta_base, "assets")
ruta_datos = os.path.join(ruta_base, "datos")

archivo_jugadores = os.path.join(ruta_datos, "jugadores.json")
archivo_facciones = os.path.join(ruta_datos, "facciones.json")


# ============================================================
# VENTANA
# ============================================================
titulo_ventana = "Defensa y Asalto de Base"
ancho_ventana = 1100
alto_ventana = 700


# ============================================================
# MAPA
# ============================================================
filas_mapa = 10
columnas_mapa = 10
tamano_casilla = 60

fila_base = 5
columna_base = 9  # la base central queda fija en el extremo derecho


# ============================================================
# ECONOMIA
# ============================================================
dinero_inicial_defensor = 300
dinero_inicial_atacante = 250
dinero_extra_por_ronda = 100

dinero_por_unidad_eliminada = 40
dinero_por_dano_a_torre = 10
dinero_por_torre_destruida = 50
dinero_por_dano_a_base = 20


# ============================================================
# PARTIDA
# ============================================================
rondas_para_ganar = 3
