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
    #R: retorna (jugador_defensor, jugador_atacante), o (None, None)
        si alguien cancela
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
            messagebox.showerror("Error", "El jugador 2 debe usar una cuenta distinta.")
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
    #S: el defensor elige primero su faccion, y al atacante le quedan
        solo las que no eligio el defensor
    #R: retorna (faccion_defensor, faccion_atacante)
    '''
    todas = []
    for nombre in datos_facciones:
        todas.append(nombre)

    faccion_defensor = elegir_faccion(jugador_defensor.usuario, todas, datos_facciones)
    if faccion_defensor is None:
        return None, None

    restantes = []
    for nombre in todas:
        if nombre != faccion_defensor:
            restantes.append(nombre)

    faccion_atacante = elegir_faccion(jugador_atacante.usuario, restantes, datos_facciones)
    return faccion_defensor, faccion_atacante


def main():
    '''
    #E: no recibe parametros
    #S: corre el juego en bucle: cada vuelta es una partida completa
        (login, roles, facciones y juego). Si los jugadores eligen
        "volver al menu", se repite; si cancelan el login, termina
    #R: no retorna nada
    '''
    seguir = True
    while seguir:
        jugador_defensor, jugador_atacante = conseguir_jugadores_y_roles()
        if jugador_defensor is None:
            return

        datos_facciones = facciones_mod.cargar_facciones()
        faccion_defensor, faccion_atacante = conseguir_facciones(
            jugador_defensor, jugador_atacante, datos_facciones)
        if faccion_defensor is None or faccion_atacante is None:
            return

        # abrir_ventana_juego devuelve True si se pidio volver al menu
        seguir = abrir_ventana_juego(jugador_defensor, jugador_atacante,
                                     faccion_defensor, faccion_atacante, datos_facciones)


def abrir_ventana_juego(jugador_defensor, jugador_atacante,
                        faccion_defensor, faccion_atacante, datos_facciones):
    '''
    #E: los dos jugadores (Jugador), sus dos facciones (str) y
        datos_facciones (dict)
    #S: crea la ventana de la partida con el tablero, el panel de
        informacion por turnos, los controles del jugador activo, y
        los botones para avanzar de fase, reiniciar o volver al menu
    #R: no retorna nada
    '''
    partida_actual = partida_mod.Partida()
    controles.limpiar_seleccion()

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

    ancho_panel = config.ancho_ventana - ancho_tablero - 60
    panel = tk.Canvas(ventana, width=ancho_panel, height=alto_tablero,
                      bg=config.color_fondo, highlightthickness=0)
    panel.pack(side="left", padx=10, pady=20, fill="both")

    icono_moneda = recursos.cargar_imagen(os.path.join(config.ruta_iconos_img, "moneda.png"))

    # Guardamos aqui los botones que cambian segun la fase para poder
    # volver a dibujarlos cada vez.
    estado = {"volver_al_menu": [False]}

    def texto_turno():
        '''
        #E: no recibe parametros
        #S: arma el texto grande que dice de quien es el turno segun la fase
        #R: retorna (titulo, color)
        '''
        if partida_actual.fase == "construccion":
            return "TURNO DEL DEFENSOR", config.color_dorado
        elif partida_actual.fase == "ataque":
            return "TURNO DEL ATACANTE", config.color_morado
        else:
            return "COMBATE EN CURSO", config.color_texto

    def dibujar_panel():
        '''
        #E: no recibe parametros
        #S: dibuja todo el panel lateral: de quien es el turno, el
            dinero y vida relevantes, la lista de controles del jugador
            activo, y lo que tiene seleccionado
        #R: no retorna nada
        '''
        panel.delete("info")
        cx = ancho_panel // 2

        # --- Cabecera: de quien es el turno ---
        titulo, color = texto_turno()
        panel.create_text(cx, 26, text=titulo, fill=color,
                          font=(config.fuente_normal, 15, "bold"), tags="info")

        panel.create_text(cx, 52, text="Ronda " + str(partida_actual.ronda_actual)
                          + "   (Def " + str(partida_actual.victorias_defensor)
                          + " - Atk " + str(partida_actual.victorias_atacante) + ")",
                          fill=config.color_texto_suave,
                          font=(config.fuente_normal, 10), tags="info")

        panel.create_line(20, 74, ancho_panel - 20, 74, fill=config.color_borde, tags="info")

        # --- Informacion segun la fase ---
        if partida_actual.fase == "construccion":
            dibujar_info_defensor(cx)
        elif partida_actual.fase == "ataque":
            dibujar_info_atacante(cx)
        else:
            dibujar_info_combate(cx)

    def dibujar_dinero(cx, y, etiqueta, cantidad, color):
        '''
        #E: cx (int) centro, y (int) altura, etiqueta (str), cantidad
            (int) de dinero, color (str)
        #S: dibuja el icono de moneda y el texto del dinero, sin que se
            encimen
        #R: no retorna nada
        '''
        if icono_moneda is not None:
            panel.create_image(40, y, image=icono_moneda, tags="info")
        panel.create_text(58, y, anchor="w", text=etiqueta + ": " + str(cantidad),
                          fill=color, font=(config.fuente_normal, 12, "bold"), tags="info")

    def dibujar_lista_controles(cx, y_inicio, lista, color):
        '''
        #E: cx (int), y_inicio (int) donde empieza la lista, lista de
            tuplas (tecla, nombre, costo), color (str) del titulo
        #S: dibuja cada control en su propia linea: [TECLA] Nombre - costo
        #R: retorna la y final usada
        '''
        y = y_inicio
        for tecla, nombre, costo in lista:
            # Recuadro de la tecla
            panel.create_rectangle(24, y - 12, 48, y + 12, fill=config.color_panel_claro,
                                   outline=color, tags="info")
            panel.create_text(36, y, text=tecla, fill=config.color_texto,
                             font=(config.fuente_normal, 11, "bold"), tags="info")
            # Nombre y costo
            panel.create_text(58, y, anchor="w", text=nombre, fill=config.color_texto,
                             font=(config.fuente_normal, 11), tags="info")
            panel.create_text(ancho_panel - 24, y, anchor="e", text=str(costo),
                             fill=config.color_dorado, font=(config.fuente_normal, 11), tags="info")
            y = y + 34
        return y

    def dibujar_seleccion(cx, y):
        '''
        #E: cx (int), y (int)
        #S: muestra que tiene seleccionado el jugador en este momento
        #R: no retorna nada
        '''
        seleccion = controles.seleccion_actual
        texto_sel = "nada" if seleccion is None else seleccion
        panel.create_text(cx, y, text="Seleccionado: " + texto_sel,
                          fill="#5ab0d8", font=(config.fuente_normal, 11, "bold"), tags="info")

    def dibujar_info_defensor(cx):
        '''
        #E: cx (int) centro del panel
        #S: muestra el dinero del defensor, sus controles y como jugar
        #R: no retorna nada
        '''
        dibujar_dinero(cx, 100, "Tu dinero", partida_actual.dinero_defensor, config.color_dorado)
        panel.create_text(cx, 130, text="Construye tu defensa", fill=config.color_texto,
                          font=(config.fuente_normal, 11), tags="info")
        panel.create_text(cx, 150, text="Elige con la tecla y haz clic en el mapa",
                          fill=config.color_texto_suave, font=(config.fuente_normal, 9), tags="info")

        y_fin = dibujar_lista_controles(cx, 185, controles.lista_controles_defensor(),
                                        config.color_dorado)
        dibujar_seleccion(cx, y_fin + 6)

    def dibujar_info_atacante(cx):
        '''
        #E: cx (int) centro del panel
        #S: muestra el dinero del atacante, sus controles y como jugar
        #R: no retorna nada
        '''
        dibujar_dinero(cx, 100, "Tu dinero", partida_actual.dinero_atacante, config.color_morado)
        panel.create_text(cx, 130, text="Compra tus unidades", fill=config.color_texto,
                          font=(config.fuente_normal, 11), tags="info")
        panel.create_text(cx, 150, text="Elige con la tecla y haz clic en una fila",
                          fill=config.color_texto_suave, font=(config.fuente_normal, 9), tags="info")

        y_fin = dibujar_lista_controles(cx, 185, controles.lista_controles_atacante(),
                                        config.color_morado)
        dibujar_seleccion(cx, y_fin + 6)

    def dibujar_info_combate(cx):
        '''
        #E: cx (int) centro del panel
        #S: durante el combate muestra la vida de la base y el dinero de
            los dos, ya que aqui no se compra ni se construye
        #R: no retorna nada
        '''
        panel.create_text(cx, 104, text="Vida de la base", fill=config.color_texto,
                          font=(config.fuente_normal, 11), tags="info")
        panel.create_text(cx, 128, text=str(partida_actual.vida_base), fill=config.color_dorado,
                          font=(config.fuente_normal, 20, "bold"), tags="info")

        unidades_vivas = 0
        for unidad in partida_actual.unidades:
            if unidad.esta_viva():
                unidades_vivas = unidades_vivas + 1
        panel.create_text(cx, 168, text="Unidades atacantes vivas: " + str(unidades_vivas),
                          fill=config.color_morado, font=(config.fuente_normal, 11), tags="info")

        panel.create_text(cx, 205, text="Presiona Siguiente turno", fill=config.color_texto_suave,
                          font=(config.fuente_normal, 10), tags="info")
        panel.create_text(cx, 225, text="para resolver el combate", fill=config.color_texto_suave,
                          font=(config.fuente_normal, 10), tags="info")

    def redibujar():
        '''
        #E: no recibe parametros
        #S: dibuja el tablero (con las imagenes del defensor) y el panel.
            Las unidades del atacante solo se muestran cuando ya no es la
            fase de construccion (asi cada jugador ve solo lo suyo)
        #R: no retorna nada
        '''
        tablero.dibujar_tablero(canvas, partida_actual.tablero, faccion_defensor, datos_facciones)
        if partida_actual.fase != "construccion":
            tablero.dibujar_unidades(canvas, partida_actual.unidades, faccion_atacante, datos_facciones)
        dibujar_panel()
        dibujar_botones_fase()

    def mapa_pieza_a_imagen(seleccion):
        '''
        #E: seleccion (str) tipo seleccionado por el jugador (ej
            "basica", "muro", "tanque")
        #S: traduce el tipo seleccionado al nombre exacto de archivo de
            imagen dentro de la carpeta de la faccion
        #R: retorna el nombre de archivo (str), o None si no aplica
        '''
        if seleccion in ("basica", "pesada", "magica"):
            return "torre_" + seleccion
        elif seleccion == "muro":
            return "muro"
        elif seleccion == "soldado":
            return "unidad_soldado"
        elif seleccion == "tanque":
            return "unidad_tanque"
        elif seleccion == "rapida":
            return "unidad_rapida"
        return None

    def mover_mouse_en_canvas(evento):
        '''
        #E: evento de Tkinter con la posicion actual del mouse
        #S: si hay algo seleccionado, dibuja sobre el tablero una vista
            previa de donde se va a colocar: en construccion resalta la
            casilla exacta, en ataque resalta toda la fila (porque ahi
            se compra en cualquier punto de la fila)
        #R: no retorna nada
        '''
        canvas.delete("vista_previa")

        seleccion = controles.seleccion_actual
        if seleccion is None or partida_actual.fase == "combate":
            return

        columna = evento.x // config.tamano_casilla
        fila = evento.y // config.tamano_casilla
        if fila < 0 or fila >= config.filas_mapa or columna < 0 or columna >= config.columnas_mapa:
            return

        nombre_archivo = mapa_pieza_a_imagen(seleccion)
        if nombre_archivo is None:
            return

        if partida_actual.fase == "construccion":
            carpeta = datos_facciones[faccion_defensor]["carpeta_assets"]
            libre = partida_actual.tablero[fila][columna] is None
            tablero.dibujar_resaltado_casilla(canvas, fila, columna, config.color_dorado, libre)
            if libre:
                tablero.dibujar_vista_previa_pieza(canvas, fila, columna, carpeta, nombre_archivo, True)

        elif partida_actual.fase == "ataque":
            carpeta = datos_facciones[faccion_atacante]["carpeta_assets"]
            tablero.dibujar_resaltado_fila(canvas, fila, config.color_morado)
            tablero.dibujar_vista_previa_pieza(canvas, fila, 0, carpeta, nombre_archivo, True)

    def guardar_resultado_partida(ganador):
        '''
        #E: ganador (str), "defensor" o "atacante"
        #S: suma la victoria al jugador del rol ganador y guarda los dos
            jugadores en el archivo
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
        #E: evento de Tkinter con la posicion del clic
        #S: en construccion coloca torre/muro; en ataque compra unidad.
            En combate, el clic en el mapa no hace nada
        #R: no retorna nada
        '''
        columna = evento.x // config.tamano_casilla
        fila = evento.y // config.tamano_casilla

        if fila < 0 or fila >= config.filas_mapa or columna < 0 or columna >= config.columnas_mapa:
            return

        seleccion = controles.seleccion_actual
        if seleccion is None:
            return

        exito = False

        if partida_actual.fase == "construccion":
            if seleccion == "muro":
                exito = partida_actual.colocar_muro(fila, columna)
            elif seleccion in ("basica", "pesada", "magica"):
                exito = partida_actual.colocar_torre(seleccion, fila, columna)

        elif partida_actual.fase == "ataque":
            if seleccion in ("soldado", "tanque", "rapida"):
                exito = partida_actual.comprar_unidad(seleccion, fila)

        if exito:
            recursos.reproducir_sonido("colocar")
        else:
            recursos.reproducir_sonido("error")

        redibujar()

    def tecla_presionada(evento):
        '''
        #E: evento de Tkinter con la tecla presionada
        #S: actualiza la seleccion segun la fase, refresca el panel, y
            vuelve a dibujar la vista previa en la posicion actual del
            mouse (asi se ve de inmediato la nueva pieza elegida)
        #R: no retorna nada
        '''
        controles.procesar_tecla(evento.char, partida_actual.fase)
        dibujar_panel()

        x_pantalla, y_pantalla = ventana.winfo_pointerxy()
        x_relativo = x_pantalla - canvas.winfo_rootx()
        y_relativo = y_pantalla - canvas.winfo_rooty()

        evento_simulado = type("EventoSimulado", (), {"x": x_relativo, "y": y_relativo})()
        mover_mouse_en_canvas(evento_simulado)

    # ====================================================
    # CAMBIOS DE FASE (con validacion)
    # ====================================================
    def terminar_construccion():
        '''
        #E: no recibe parametros
        #S: pasa de construccion a ataque, limpia la seleccion para que
            el atacante empiece de cero
        #R: no retorna nada
        '''
        partida_actual.fase = "ataque"
        controles.limpiar_seleccion()
        recursos.reproducir_sonido("click")
        redibujar()

    def terminar_ataque():
        '''
        #E: no recibe parametros
        #S: no deja pasar a combate si el atacante no compro ninguna
            unidad; si compro al menos una, pasa a la fase de combate
        #R: no retorna nada
        '''
        hay_unidades = len(partida_actual.unidades) > 0
        if not hay_unidades:
            recursos.reproducir_sonido("error")
            messagebox.showinfo("Espera", "El atacante debe comprar al menos una unidad antes del combate.")
            return

        partida_actual.fase = "combate"
        controles.limpiar_seleccion()
        recursos.reproducir_sonido("click")
        redibujar()

    def siguiente_turno():
        '''
        #E: no recibe parametros
        #S: solo funciona en fase de combate. Avanza un turno, suena el
            disparo y la destruccion si murio alguien, y revisa si la
            ronda o la partida terminaron
        #R: no retorna nada
        '''
        if partida_actual.fase != "combate":
            recursos.reproducir_sonido("error")
            messagebox.showinfo("Espera", "Primero termina la construccion y la fase de ataque.")
            return

        vivas_antes = 0
        for unidad in partida_actual.unidades:
            if unidad.esta_viva():
                vivas_antes = vivas_antes + 1

        partida_actual.avanzar_turno_combate()
        recursos.reproducir_sonido("disparo")
        redibujar()

        vivas_despues = 0
        for unidad in partida_actual.unidades:
            if unidad.esta_viva():
                vivas_despues = vivas_despues + 1
        if vivas_despues < vivas_antes:
            recursos.reproducir_sonido("destruccion")

        ganador_ronda = partida_actual.verificar_ganador_ronda()
        if ganador_ronda is not None:
            recursos.reproducir_sonido("victoria")
            messagebox.showinfo("Ronda terminada", "Gano la ronda: " + ganador_ronda)
            partida_actual.iniciar_nueva_ronda(ganador_ronda)
            controles.limpiar_seleccion()

            ganador_partida = partida_actual.hay_ganador_de_partida()
            if ganador_partida is not None:
                if ganador_partida == "defensor":
                    nombre = jugador_defensor.usuario
                else:
                    nombre = jugador_atacante.usuario
                messagebox.showinfo("Partida terminada",
                                    "Gano: " + nombre + " (" + ganador_partida + ")")
                guardar_resultado_partida(ganador_partida)

            redibujar()

    def reiniciar_partida():
        '''
        #E: no recibe parametros
        #S: pregunta si esta seguro y, si acepta, deja la partida como
            nueva desde la ronda 1
        #R: no retorna nada
        '''
        if messagebox.askyesno("Reiniciar", "Seguro que quieres reiniciar la partida desde cero?"):
            partida_actual.reiniciar()
            controles.limpiar_seleccion()
            redibujar()

    def volver_al_menu():
        '''
        #E: no recibe parametros
        #S: pregunta si esta seguro y, si acepta, cierra la ventana de
            juego para regresar al menu principal
        #R: no retorna nada
        '''
        if messagebox.askyesno("Volver al menu", "Seguro que quieres salir al menu principal?"):
            estado["volver_al_menu"][0] = True
            ventana.destroy()

    def abrir_ajustes():
        mostrar_ajustes(ventana)

    # ====================================================
    # BOTONES (cambian segun la fase)
    # ====================================================
    def dibujar_botones_fase():
        '''
        #E: no recibe parametros
        #S: borra los botones anteriores y dibuja los que correspondan a
            la fase actual, mas los botones fijos de reiniciar, ajustes
            y menu
        #R: no retorna nada
        '''
        panel.delete("boton")
        cx = ancho_panel // 2
        # Zona de botones de accion principal (segun fase)
        y_accion = 410

        if partida_actual.fase == "construccion":
            crear_boton(cx, y_accion, "Terminar construccion", terminar_construccion, "azul")
        elif partida_actual.fase == "ataque":
            crear_boton(cx, y_accion, "Empezar combate", terminar_ataque, "rojo")
        else:
            crear_boton(cx, y_accion, "Siguiente turno", siguiente_turno, "verde")

        # Botones fijos abajo, con suficiente separacion
        crear_boton(cx, 482, "Reiniciar partida", reiniciar_partida, "gris", ancho=200, tam=11)
        crear_boton(cx - 62, 548, "Menu", volver_al_menu, "gris", ancho=112, tam=10)
        crear_boton(cx + 62, 548, "Ajustes", abrir_ajustes, "gris", ancho=112, tam=10)

    def crear_boton(x, y, texto, accion, color, ancho=220, tam=12):
        '''
        #E: x, y (int) centro del boton, texto (str), accion (funcion),
            color (str), ancho (int), tam (int) de la fuente
        #S: crea un BotonImagen marcado con la etiqueta "boton" para
            poder borrarlo al cambiar de fase
        #R: no retorna nada
        '''
        boton = BotonImagen(panel, x, y, texto, accion, color=color, ancho=ancho, tam_fuente=tam)
        panel.addtag_withtag("boton", boton.id_imagen)
        panel.addtag_withtag("boton", boton.id_texto)

    canvas.bind("<Button-1>", clic_en_canvas)
    canvas.bind("<Motion>", mover_mouse_en_canvas)
    canvas.bind("<Leave>", lambda evento: canvas.delete("vista_previa"))
    ventana.bind("<Key>", tecla_presionada)

    redibujar()
    ventana.wait_window()
    recursos.detener_musica()

    return estado["volver_al_menu"][0]


if __name__ == "__main__":
    main()
    raiz = recursos.obtener_raiz()
    raiz.destroy()
