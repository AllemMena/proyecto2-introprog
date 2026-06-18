'''
Archivo principal del proyecto Defensa y Asalto de Base.
Version 0: solo abre la ventana base para confirmar que la
estructura del proyecto funciona. Aqui se conectara despues
el flujo completo: login, seleccion de faccion, partida.
'''

import tkinter as tk
import config


def main():
    '''
    #E: no recibe parametros
    #S: crea la ventana principal de Tkinter con el titulo y tamano definidos en config
    #R: no retorna nada
    '''
    ventana = tk.Tk()
    ventana.title(config.titulo_ventana)
    ventana.geometry(f"{config.ancho_ventana}x{config.alto_ventana}")

    etiqueta = tk.Label(
        ventana,
        text="Defensa y Asalto de Base\n(version 0 - en construccion)",
        font=("Arial", 18),
    )
    etiqueta.pack(expand=True)

    ventana.mainloop()


if __name__ == "__main__":
    main()
