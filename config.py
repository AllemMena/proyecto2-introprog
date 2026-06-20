#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import os


# ============================================================
# RUTAS
# ============================================================
ruta_base = os.path.dirname(os.path.abspath(__file__))
ruta_assets = os.path.join(ruta_base, "assets")
ruta_datos = os.path.join(ruta_base, "datos")

ruta_facciones_img = os.path.join(ruta_assets, "facciones")
ruta_mapa_img = os.path.join(ruta_assets, "mapa")
ruta_ui_img = os.path.join(ruta_assets, "ui")
ruta_iconos_img = os.path.join(ruta_assets, "iconos")
ruta_sonidos = os.path.join(ruta_assets, "sonidos")

archivo_jugadores = os.path.join(ruta_datos, "jugadores.json")
archivo_facciones = os.path.join(ruta_datos, "facciones.json")


# ============================================================
# VENTANA
# ============================================================
titulo_ventana = "Defensa y Asalto de Base"
ancho_ventana = 1100
alto_ventana = 700

# Paleta de colores usada en toda la interfaz
color_fondo = "#11131a"
color_panel = "#1c1f2b"
color_panel_claro = "#262a38"
color_texto = "#e8e8ec"
color_texto_suave = "#9aa0b0"
color_dorado = "#d4af6a"
color_morado = "#a86bd6"
color_borde = "#2a2e3d"
color_canvas = "#181a24"

# Fuente del titulo. Si no esta instalada, Tkinter usa una por defecto.
fuente_titulo = "Cinzel"
fuente_normal = "Segoe UI"


# ============================================================
# AUDIO
# ============================================================
volumen_efectos = 0.6
volumen_musica = 0.4


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
# BASE Y MUROS
# ============================================================
vida_base = 300
costo_muro = 30
vida_muro = 50


# ============================================================
# PARTIDA
# ============================================================
rondas_para_ganar = 3
