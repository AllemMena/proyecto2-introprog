#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import os
import tkinter as tk
import config
import recursos


def ruta_boton(color):
    '''
    #E: color (str): "azul", "gris", "rojo", "verde" o "amarillo"
    #S: arma la ruta del archivo de imagen del boton de ese color
    #R: retorna la ruta (str)
    '''
    return os.path.join(config.ruta_ui_img, "boton_" + color + ".png")


class BotonImagen:
    '''
    Un boton dibujado sobre un Canvas: una imagen de fondo con el texto
    encima, centrado. Cambia un poco de brillo al pasar el mouse y
    reproduce un sonido al hacer clic. Se usa para que los botones se
    vean iguales en todas las ventanas y el texto nunca se sobreponga.
    '''

    def __init__(self, canvas, x, y, texto, accion, color="azul",
                 ancho=220, alto=58, tam_fuente=13):
        '''
        #E: canvas (tk.Canvas) donde se dibuja, x e y (int) del centro
            del boton, texto (str), accion (funcion) que se llama al
            hacer clic, color (str) del boton, ancho y alto (int),
            tam_fuente (int)
        #S: dibuja la imagen del boton y su texto, y conecta los
            eventos de mouse (entrar, salir, clic)
        #R: no retorna nada
        '''
        self.canvas = canvas
        self.accion = accion

        imagen = recursos.cargar_imagen(ruta_boton(color))

        if imagen is not None:
            # Subir el ancho/alto reales de la imagen para posicionar el texto
            self.id_imagen = canvas.create_image(x, y, image=imagen)
            self.tiene_imagen = True
        else:
            # Respaldo: un rectangulo de color
            colores = {"azul": "#3a8ac4", "gris": "#5a6072", "rojo": "#a83a3a",
                       "verde": "#3a9a5a", "amarillo": "#c9a24b"}
            relleno = colores.get(color, "#3a8ac4")
            self.id_imagen = canvas.create_rectangle(
                x - ancho // 2, y - alto // 2, x + ancho // 2, y + alto // 2,
                fill=relleno, outline="")
            self.tiene_imagen = False

        self.id_texto = canvas.create_text(
            x, y, text=texto, fill="white",
            font=(config.fuente_normal, tam_fuente, "bold"))

        # Conectar eventos a los dos elementos (imagen y texto)
        for id_elemento in (self.id_imagen, self.id_texto):
            canvas.tag_bind(id_elemento, "<Button-1>", self._al_hacer_clic)
            canvas.tag_bind(id_elemento, "<Enter>", self._al_entrar)
            canvas.tag_bind(id_elemento, "<Leave>", self._al_salir)

    def _al_hacer_clic(self, evento):
        recursos.reproducir_sonido("click")
        self.accion()

    def _al_entrar(self, evento):
        self.canvas.config(cursor="hand2")
        self.canvas.itemconfig(self.id_texto, fill=config.color_dorado)

    def _al_salir(self, evento):
        self.canvas.config(cursor="")
        self.canvas.itemconfig(self.id_texto, fill="white")
