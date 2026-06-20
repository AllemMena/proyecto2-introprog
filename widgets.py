#Allem Mena Joel Alpizar
#Introduccion a la programación proyecto 2

import os
import config
import recursos


def archivo_boton(color, ancho):
    '''
    #E: color (str): "azul", "gris", "rojo", "verde", "amarillo";
        ancho (int) deseado del boton
    #S: elige el archivo de boton del tamano mas cercano al ancho
        pedido. Hay tres tamanos: grande (g), mediano (m) y chico (c)
    #R: retorna la ruta del archivo de imagen del boton
    '''
    if ancho >= 215:
        sufijo = "g"
    elif ancho >= 160:
        sufijo = "m"
    else:
        sufijo = "c"
    return os.path.join(config.ruta_ui_img, "boton_" + color + "_" + sufijo + ".png")


class BotonImagen:
    '''
    Un boton dibujado sobre un Canvas: una imagen de fondo con el texto
    encima, centrado. Cambia de color el texto al pasar el mouse y
    reproduce un sonido al hacer clic. Se usa para que los botones se
    vean iguales en todas las ventanas y el texto nunca se sobreponga.
    '''

    def __init__(self, canvas, x, y, texto, accion, color="azul",
                 ancho=220, alto=52, tam_fuente=13):
        '''
        #E: canvas (tk.Canvas) donde se dibuja, x e y (int) del centro,
            texto (str), accion (funcion) al hacer clic, color (str),
            ancho y alto (int), tam_fuente (int)
        #S: dibuja la imagen del boton y su texto centrado, y conecta
            los eventos de mouse (entrar, salir, clic)
        #R: no retorna nada
        '''
        self.canvas = canvas
        self.accion = accion

        imagen = recursos.cargar_imagen(archivo_boton(color, ancho))

        if imagen is not None:
            self.id_imagen = canvas.create_image(x, y, image=imagen)
        else:
            colores = {"azul": "#3a8ac4", "gris": "#5a6072", "rojo": "#a83a3a",
                       "verde": "#3a9a5a", "amarillo": "#c9a24b"}
            relleno = colores.get(color, "#3a8ac4")
            self.id_imagen = canvas.create_rectangle(
                x - ancho // 2, y - alto // 2, x + ancho // 2, y + alto // 2,
                fill=relleno, outline="")

        self.id_texto = canvas.create_text(
            x, y, text=texto, fill="white",
            font=(config.fuente_normal, tam_fuente, "bold"))

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
