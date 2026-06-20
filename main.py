#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import os
import tkinter as tk
from tkinter import messagebox
import config
import recursos
import tablero
import controles
import partida as partida_mod
import facciones as facciones_mod
from widgets import BotonImagen
from jugador import cargar_jugadores, guardar_jugadores
from interfaz.ventana_login import abrir_ventana
from interfaz.ventana_seleccion import elegir_rol, elegir_faccion
from interfaz.ventana_ajustes import mostrar_ajustes


def conseguir_jugadores_y_roles():
    '''
    #E: no recibe parametros
    #S: pide el login de los dos jugadores (revisando que no sea la
        misma cuenta) y les asigna el rol contrario entre ellos
    #R: retorna una tupla (jugador_defensor, jugador_atacante), o
        (None, None) si alguien cerro una ventana sin iniciar sesion
    '''
    jugador1 = abrir_ventana("Jugador 1 - Inicia sesion")
    if jugador1 is None:
        return None, None

    rol_jugador1 = elegir_rol(jugador1.usuario)
    if rol_jugador1 is None:
        return None, None

    if rol_jugador1 == "defensor":
        rol_jugador2 = "atacante"
    else:
        rol_jugador2 = "defensor"

    jugador2 = None
    while jugador2 is None:
        candidato = abrir_ventana("Jugador 2 (" + rol_jugador2 + ") - Inicia sesion")
        if candidato is None:
            return None, None

        if candidato.usuario == jugador1.usuario:
            messagebox.showerror("Error", "El jugador 2 debe usar una cuenta distinta a la del jugador 1.")
        else:
            jugador2 = candidato

    if rol_jugador1 == "defensor":
        return jugador1, jugador2
    else:
        return jugador2, jugador1


def conseguir_facciones(jugador_defensor, jugador_atacante, datos_facciones):
    '''
    #E: jugador_defensor (Jugador), jugador_atacante (Jugador),
        datos_facciones (dict)
    #S: deja que el defensor elija primero su faccion, y al atacante
        le muestra solo las que quedan disponibles
    #R: retorna una tupla (faccion_defensor, faccion_atacante)
    '''
    todas_las_facciones = []
    for nombre_faccion in datos_facciones:
        todas_las_facciones.append(nombre_faccion)

    faccion_defensor = elegir_faccion(jugador_defensor.usuario, todas_las_facciones, datos_facciones)

    facciones_restantes = []
    for nombre_faccion in todas_las_facciones:
        if nombre_faccion != faccion_defensor:
            facciones_restantes.append(nombre_faccion)

    faccion_atacante = elegir_faccion(jugador_atacante.usuario, facciones_restantes, datos_facciones)

    return faccion_defensor, faccion_atacante


def main():
    '''
    #E: no recibe parametros
    #S: corre todo el flujo: login de los dos jugadores, roles,
        facciones, y abre la ventana del juego completa
    #R: no retorna nada
    '''
    jugador_defensor, jugador_atacante = conseguir_jugadores_y_roles()
    if jugador_defensor is None:
        return

    datos_facciones = facciones_mod.cargar_facciones()
    faccion_defensor, faccion_atacante = conseguir_facciones(jugador_defensor, jugador_atacante, datos_facciones)
    if faccion_defensor is None or faccion_atacante is None:
        return

    partida_actual = partida_mod.Partida()

    ventana = tk.Toplevel(recursos.obtener_raiz())
    ventana.title(config.titulo_ventana)
    ventana.geometry(str(config.ancho_ventana) + "x" + str(config.alto_ventana))
    ventana.configure(bg=config.color_fondo)
    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)

    recursos.reproducir_musica("musica_partida.mp3")

    ancho_tablero = config.columnas_mapa * config.tamano_casilla
    alto_tablero = config.filas_mapa * config.tamano_casilla

    canvas = tk.Canvas(ventana, width=ancho_tablero, height=alto_tablero,
                       bg=config.color_canvas, highlightthickness=0)
    canvas.pack(side="left", padx=20, pady=20)

    # Panel lateral, tambien un canvas para poder dibujar el icono de
    # moneda y los botones de imagen con buena estetica.
    ancho_panel = config.ancho_ventana - ancho_tablero - 60
    panel = tk.Canvas(ventana, width=ancho_panel, height=alto_tablero,
                      bg=config.color_fondo, highlightthickness=0)
    panel.pack(side="left", padx=10, pady=20, fill="both")

    icono_moneda = recursos.cargar_imagen(os.path.join(config.ruta_iconos_img, "moneda.png"))

    def actualizar_panel():
        '''
        #E: no recibe parametros
        #S: vuelve a dibujar todo el panel lateral con la informacion
            actual de la partida: jugadores, fase, dinero, vida y ronda
        #R: no retorna nada
        '''
        panel.delete("info")
        cx = ancho_panel // 2

        # Jugadores y facciones
        panel.create_text(cx, 20, text="Defensor", fill=config.color_dorado,
                          font=(config.fuente_normal, 11, "bold"), tags="info")
        panel.create_text(cx, 40, text=jugador_defensor.usuario + " - " + faccion_defensor,
                          fill=config.color_texto, font=(config.fuente_normal, 10), tags="info")
        panel.create_text(cx, 64, text="Atacante", fill=config.color_morado,
                          font=(config.fuente_normal, 11, "bold"), tags="info")
        panel.create_text(cx, 84, text=jugador_atacante.usuario + " - " + faccion_atacante,
                          fill=config.color_texto, font=(config.fuente_normal, 10), tags="info")

        panel.create_line(20, 108, ancho_panel - 20, 108, fill=config.color_borde, tags="info")

        # Fase
        panel.create_text(cx, 132, text="Fase: " + partida_actual.fase,
                          fill=config.color_texto, font=(config.fuente_normal, 13, "bold"), tags="info")

        # Dinero con icono de moneda
        if icono_moneda is not None:
            panel.create_image(cx - 95, 168, image=icono_moneda, tags="info")
            panel.create_image(cx - 95, 196, image=icono_moneda, tags="info")
        panel.create_text(cx - 75, 168, anchor="w", text="Defensor: " + str(partida_actual.dinero_defensor),
                          fill=config.color_dorado, font=(config.fuente_normal, 11), tags="info")
        panel.create_text(cx - 75, 196, anchor="w", text="Atacante: " + str(partida_actual.dinero_atacante),
                          fill=config.color_morado, font=(config.fuente_normal, 11), tags="info")

        # Vida de la base
        panel.create_text(cx, 228, text="Vida de la base: " + str(partida_actual.vida_base),
                          fill=config.color_texto, font=(config.fuente_normal, 11), tags="info")

        # Ronda y marcador
        panel.create_text(cx, 256, text="Ronda " + str(partida_actual.ronda_actual),
                          fill=config.color_texto, font=(config.fuente_normal, 11, "bold"), tags="info")
        panel.create_text(cx, 278, text="Defensor " + str(partida_actual.victorias_defensor)
                          + "  -  " + str(partida_actual.victorias_atacante) + " Atacante",
                          fill=config.color_texto_suave, font=(config.fuente_normal, 10), tags="info")

        # Que esta seleccionado
        seleccion = controles.seleccion_actual
        texto_sel = "nada" if seleccion is None else seleccion
        panel.create_text(cx, 308, text="Seleccionado: " + texto_sel,
                          fill="#5ab0d8", font=(config.fuente_normal, 10), tags="info")

        panel.create_line(20, 330, ancho_panel - 20, 330, fill=config.color_borde, tags="info")

    def redibujar():
        '''
        #E: no recibe parametros
        #S: vuelve a dibujar el tablero con las imagenes del defensor,
            las unidades con las del atacante, y refresca el panel
        #R: no retorna nada
        '''
        tablero.dibujar_tablero(canvas, partida_actual.tablero, faccion_defensor, datos_facciones)
        tablero.dibujar_unidades(canvas, partida_actual.unidades, faccion_atacante, datos_facciones)
        actualizar_panel()

    def guardar_resultado_partida(ganador):
        '''
        #E: ganador (str), "defensor" o "atacante"
        #S: le suma la victoria al jugador que tenia ese rol, y guarda
            el cambio de los dos jugadores en el archivo
        #R: no retorna nada
        '''
        if ganador == "defensor":
            jugador_defensor.sumar_victoria("defensor")
        else:
            jugador_atacante.sumar_victoria("atacante")

        datos_jugadores = cargar_jugadores()
        datos_jugadores[jugador_defensor.usuario] = jugador_defensor.a_diccionario()
        datos_jugadores[jugador_atacante.usuario] = jugador_atacante.a_diccionario()
        guardar_jugadores(datos_jugadores)

    def clic_en_canvas(evento):
        '''
        #E: evento (de Tkinter), con la posicion x, y del clic
        #S: calcula la fila y columna del clic y, segun la fase y lo
            que este seleccionado, coloca torre/muro o compra unidad.
            Reproduce un sonido segun si la accion se pudo o no
        #R: no retorna nada
        '''
        columna = evento.x // config.tamano_casilla
        fila = evento.y // config.tamano_casilla

        if fila < 0 or fila >= config.filas_mapa or columna < 0 or columna >= config.columnas_mapa:
            return

        tipo_seleccionado = controles.seleccion_actual
        if tipo_seleccionado is None:
            return

        exito = False

        if partida_actual.fase == "construccion":
            if tipo_seleccionado == "muro":
                exito = partida_actual.colocar_muro(fila, columna)
            elif tipo_seleccionado in ("basica", "pesada", "magica"):
                exito = partida_actual.colocar_torre(tipo_seleccionado, fila, columna)

        elif partida_actual.fase == "ataque":
            if tipo_seleccionado in ("soldado", "tanque", "rapida"):
                exito = partida_actual.comprar_unidad(tipo_seleccionado, fila)

        if exito:
            recursos.reproducir_sonido("colocar")
        else:
            recursos.reproducir_sonido("error")

        redibujar()

    def tecla_presionada(evento):
        controles.procesar_tecla(evento.char)
        actualizar_panel()

    def pasar_a_ataque():
        partida_actual.fase = "ataque"
        recursos.reproducir_sonido("click")
        redibujar()

    def iniciar_combate():
        partida_actual.fase = "combate"
        recursos.reproducir_sonido("click")
        redibujar()

    def siguiente_turno():
        '''
        #E: no recibe parametros (se llama desde el boton)
        #S: avanza un turno de combate, redibuja, y revisa si la ronda
            o la partida completa terminaron, con sus sonidos
        #R: no retorna nada
        '''
        vivas_antes = 0
        for u in partida_actual.unidades:
            if u.esta_viva():
                vivas_antes = vivas_antes + 1

        partida_actual.avanzar_turno_combate()
        recursos.reproducir_sonido("disparo")
        redibujar()

        vivas_despues = 0
        for u in partida_actual.unidades:
            if u.esta_viva():
                vivas_despues = vivas_despues + 1
        if vivas_despues < vivas_antes:
            recursos.reproducir_sonido("destruccion")

        ganador_ronda = partida_actual.verificar_ganador_ronda()
        if ganador_ronda is not None:
            recursos.reproducir_sonido("victoria")
            messagebox.showinfo("Ronda terminada", "Gano la ronda: " + ganador_ronda)
            partida_actual.iniciar_nueva_ronda(ganador_ronda)

            ganador_partida = partida_actual.hay_ganador_de_partida()
            if ganador_partida is not None:
                if ganador_partida == "defensor":
                    nombre_ganador = jugador_defensor.usuario
                else:
                    nombre_ganador = jugador_atacante.usuario

                messagebox.showinfo("Partida terminada",
                                    "Gano la partida: " + nombre_ganador + " (" + ganador_partida + ")")
                guardar_resultado_partida(ganador_partida)

            redibujar()

    def abrir_ajustes():
        mostrar_ajustes(ventana)

    # --- Botones del panel (imagenes en el canvas del panel) ---
    base_y = 365
    BotonImagen(panel, ancho_panel // 2, base_y, "Pasar a ataque", pasar_a_ataque,
                color="azul", ancho=220, tam_fuente=12)
    BotonImagen(panel, ancho_panel // 2, base_y + 60, "Iniciar combate", iniciar_combate,
                color="rojo", ancho=220, tam_fuente=12)
    BotonImagen(panel, ancho_panel // 2, base_y + 120, "Siguiente turno", siguiente_turno,
                color="verde", ancho=220, tam_fuente=12)
    BotonImagen(panel, ancho_panel // 2, base_y + 195, "Ajustes", abrir_ajustes,
                color="gris", ancho=160, tam_fuente=11)

    canvas.bind("<Button-1>", clic_en_canvas)
    ventana.bind("<Key>", tecla_presionada)

    redibujar()
    ventana.wait_window()
    recursos.detener_musica()


if __name__ == "__main__":
    main()
    # Al terminar todo el juego, cerrar la ventana raiz oculta
    raiz = recursos.obtener_raiz()
    raiz.destroy()
