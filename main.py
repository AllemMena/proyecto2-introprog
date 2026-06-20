'''
Archivo principal del proyecto Defensa y Asalto de Base.
Login -> ventana del juego con el tablero, el dinero, las fases de
construccion y ataque, y el combate por turnos.
Falta: seleccion de faccion y la ventana de ranking.
'''

import tkinter as tk
from tkinter import messagebox
import config
import tablero
import controles
import partida as partida_mod
from interfaz.ventana_login import abrir_ventana, cargar_jugadores, guardar_jugadores


def main():
    '''
    #E: no recibe parametros
    #S: muestra el login, y si alguien entra, abre la ventana del
        juego completa: tablero, panel de informacion, botones de
        fase, clics en el mapa y teclas para seleccionar que colocar
    #R: no retorna nada
    '''
    jugador_actual = abrir_ventana()

    if jugador_actual is None:
        return

    partida_actual = partida_mod.Partida()

    ventana = tk.Tk()
    ventana.title(config.titulo_ventana + " - " + jugador_actual.usuario)
    ventana.geometry(f"{config.ancho_ventana}x{config.alto_ventana}")
    ventana.configure(bg="#0d0d12")

    ancho_tablero = config.columnas_mapa * config.tamano_casilla
    alto_tablero = config.filas_mapa * config.tamano_casilla

    canvas = tk.Canvas(
        ventana,
        width=ancho_tablero,
        height=alto_tablero,
        bg="#1a1a24",
        highlightthickness=0,
    )
    canvas.pack(side="left", padx=20, pady=20)

    panel = tk.Frame(ventana, bg="#0d0d12")
    panel.pack(side="left", padx=10, pady=20, fill="y")

    etiqueta_fase = tk.Label(panel, bg="#0d0d12", fg="white", font=("Arial", 12, "bold"))
    etiqueta_fase.pack(pady=(0, 10))

    etiqueta_dinero_defensor = tk.Label(panel, bg="#0d0d12", fg="#c9a24b", font=("Arial", 11))
    etiqueta_dinero_defensor.pack()

    etiqueta_dinero_atacante = tk.Label(panel, bg="#0d0d12", fg="#7a3a8a", font=("Arial", 11))
    etiqueta_dinero_atacante.pack()

    etiqueta_vida_base = tk.Label(panel, bg="#0d0d12", fg="white", font=("Arial", 11))
    etiqueta_vida_base.pack()

    etiqueta_ronda = tk.Label(panel, bg="#0d0d12", fg="white", font=("Arial", 11))
    etiqueta_ronda.pack(pady=(0, 10))

    etiqueta_seleccion = tk.Label(panel, bg="#0d0d12", fg="#5ab0d8", font=("Arial", 10))
    etiqueta_seleccion.pack(pady=(0, 10))

    def actualizar_panel():
        '''
        #E: no recibe parametros
        #S: actualiza el texto de todas las etiquetas del panel segun
            el estado actual de la partida
        #R: no retorna nada
        '''
        etiqueta_fase.config(text="Fase: " + partida_actual.fase)
        etiqueta_dinero_defensor.config(text="Dinero defensor: " + str(partida_actual.dinero_defensor))
        etiqueta_dinero_atacante.config(text="Dinero atacante: " + str(partida_actual.dinero_atacante))
        etiqueta_vida_base.config(text="Vida de la base: " + str(partida_actual.vida_base))
        etiqueta_ronda.config(
            text="Ronda " + str(partida_actual.ronda_actual)
            + " - Defensor " + str(partida_actual.victorias_defensor)
            + " / Atacante " + str(partida_actual.victorias_atacante)
        )
        etiqueta_seleccion.config(text="Seleccionado: " + str(controles.seleccion_actual))

    def redibujar():
        '''
        #E: no recibe parametros
        #S: vuelve a dibujar el tablero y las unidades, y actualiza el panel
        #R: no retorna nada
        '''
        tablero.dibujar_tablero(canvas, partida_actual.tablero)
        tablero.dibujar_unidades(canvas, partida_actual.unidades)
        actualizar_panel()

    def guardar_victoria_de_partida(ganador):
        '''
        #E: ganador (str), "defensor" o "atacante"
        #S: suma la victoria al jugador que tiene la sesion iniciada
            y guarda el cambio en el archivo de jugadores
        #R: no retorna nada
        '''
        jugador_actual.sumar_victoria(ganador)
        datos_jugadores = cargar_jugadores()
        datos_jugadores[jugador_actual.usuario] = jugador_actual.a_diccionario()
        guardar_jugadores(datos_jugadores)

    def clic_en_canvas(evento):
        '''
        #E: evento (de Tkinter), contiene la posicion x, y del clic
        #S: calcula la fila y columna donde cayo el clic, y segun la
            fase y lo que este seleccionado con el teclado, coloca una
            torre, un muro, o compra una unidad
        #R: no retorna nada
        '''
        columna = evento.x // config.tamano_casilla
        fila = evento.y // config.tamano_casilla

        if fila < 0 or fila >= config.filas_mapa or columna < 0 or columna >= config.columnas_mapa:
            return

        tipo_seleccionado = controles.seleccion_actual
        if tipo_seleccionado is None:
            return

        if partida_actual.fase == "construccion":
            if tipo_seleccionado == "muro":
                partida_actual.colocar_muro(fila, columna)
            elif tipo_seleccionado in ("basica", "pesada", "magica"):
                partida_actual.colocar_torre(tipo_seleccionado, fila, columna)

        elif partida_actual.fase == "ataque":
            if tipo_seleccionado in ("soldado", "tanque", "rapida"):
                partida_actual.comprar_unidad(tipo_seleccionado, fila)

        redibujar()

    def tecla_presionada(evento):
        controles.procesar_tecla(evento.char)
        actualizar_panel()

    def pasar_a_ataque():
        partida_actual.fase = "ataque"
        redibujar()

    def iniciar_combate():
        partida_actual.fase = "combate"
        redibujar()

    def siguiente_turno():
        '''
        #E: no recibe parametros (se llama desde el boton)
        #S: avanza un turno de combate, redibuja, y revisa si la ronda
            o la partida completa ya terminaron
        #R: no retorna nada
        '''
        partida_actual.avanzar_turno_combate()
        redibujar()

        ganador_ronda = partida_actual.verificar_ganador_ronda()
        if ganador_ronda is not None:
            messagebox.showinfo("Ronda terminada", "Gano la ronda: " + ganador_ronda)
            partida_actual.iniciar_nueva_ronda(ganador_ronda)

            ganador_partida = partida_actual.hay_ganador_de_partida()
            if ganador_partida is not None:
                messagebox.showinfo("Partida terminada", "Gano la partida: " + ganador_partida)
                guardar_victoria_de_partida(ganador_partida)

            redibujar()

    boton_pasar_ataque = tk.Button(panel, text="Pasar a fase de ataque", command=pasar_a_ataque, bg="#2a5a7a", fg="white")
    boton_pasar_ataque.pack(pady=5, fill="x")

    boton_iniciar_combate = tk.Button(panel, text="Iniciar combate", command=iniciar_combate, bg="#7a1a1a", fg="white")
    boton_iniciar_combate.pack(pady=5, fill="x")

    boton_siguiente_turno = tk.Button(panel, text="Siguiente turno", command=siguiente_turno, bg="#5a4a32", fg="white")
    boton_siguiente_turno.pack(pady=5, fill="x")

    canvas.bind("<Button-1>", clic_en_canvas)
    ventana.bind("<Key>", tecla_presionada)

    redibujar()
    ventana.mainloop()


if __name__ == "__main__":
    main()
