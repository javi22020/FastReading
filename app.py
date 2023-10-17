import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkextrafont import Font
from fontTools import ttLib
import pyttsx3
import os
import yaml
class App:
    def __init__(self):
        # Creo la ventana y la fuente
        self.window = tk.Tk()
        self.ruta_config = "assets/config.yaml"
        self.ajustes = yaml.safe_load(open(self.ruta_config, "r"))
        self.estilo = ttk.Style(self.window)
        self.text = "Este es un texto de prueba, escribe otro texto en la pestaña 'Escribir'"
        self.palabra_actual = ""
        self.tema_oscuro = self.ajustes["tema-oscuro"]
        self.tts = pyttsx3.init()
        self.voz_activada = self.ajustes["voz"]
        self.font_size = 72
        self.carpeta_fuentes = self.ajustes["carpeta-fuentes"]
        self.lista_fuentes = [f.split(".")[0] for f in os.listdir(self.carpeta_fuentes)]
        self.lista_rutas_fuentes = [self.carpeta_fuentes + f for f in os.listdir(self.carpeta_fuentes)]
        self.dict_fuentes = dict(zip(self.lista_fuentes, self.lista_rutas_fuentes))
        self.fuente_selec = self.ajustes["fuente-selec"]
        self.font = Font(root=self.window, file=self.dict_fuentes[self.fuente_selec], family=ttLib.TTFont(self.dict_fuentes[self.fuente_selec])['name'].getDebugName(1), size=self.font_size)
        self.index = 0
        self.vel = 5
        self.notebook = ttk.Notebook(master=self.window)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        # Tab Leer
        self.notebook.add(self.tab1, text="Leer")
        self.etiqueta_lectura = ttk.Label(self.tab1, text="Pulsa 'Iniciar'", font=self.font)
        self.btn_comenzar = ttk.Button(self.tab1, text="Iniciar", command=self.start_reading)
        self.slider_vel = ttk.Scale(self.tab1, orient='horizontal', from_=0, to=120, command=self.set_speed, value=self.vel, length=350)
        self.etiqueta_vel = ttk.Label(self.tab1, text="Velocidad (palabras por minuto) - " + str(self.vel))
        self.etiqueta_lectura.pack(anchor="center", expand=True)
        self.btn_comenzar.pack(anchor="center")
        self.slider_vel.pack(anchor="center", fill="x")
        self.etiqueta_vel.pack(anchor="center")
        # Tab Escribir
        self.notebook.add(self.tab2, text="Escribir")
        self.cuadro_texto = ttk.Entry(self.tab2)
        self.enviar_texto = ttk.Button(self.tab2, text="Enviar texto", command=self.enviar_texto)
        self.cuadro_texto.pack(fill="x", ipadx=15, ipady=15)
        self.enviar_texto.pack(anchor="center")
        # Tab Ajustes
        self.notebook.add(self.tab3, text="Ajustes")
        self.etiqueta_prueba = ttk.Label(self.tab3, text="Palabra", font=self.font)
        self.selector_fuente = ttk.Combobox(self.tab3, values=self.lista_fuentes, state="readonly")
        self.btn_carpeta_fuentes = ttk.Button(self.tab3, text="Cargar carpeta de fuentes", command=self.pedir_carpeta_fuentes)
        if self.voz_activada:
            texto_voz = "Voz activada"
        else:
            texto_voz = "Voz desactivada"
        self.btn_voz = ttk.Button(self.tab3, text=texto_voz, command=self.cambiar_voz)
        if self.tema_oscuro:
            texto_tema = "Tema oscuro"
            self.ajustar_tema_oscuro()
        else:
            texto_tema = "Tema claro"
            self.ajustar_tema_claro()
        self.btn_tema = ttk.Button(self.tab3, text=texto_tema, command=self.cambiar_tema)
        self.btn_guardar_ajustes = ttk.Button(self.tab3, text="Aplicar ajustes", command=self.actualizar_ajustes)
        self.etiqueta_prueba.pack(anchor="center")
        self.selector_fuente.pack(anchor="center")
        self.btn_carpeta_fuentes.pack(anchor="center")
        self.btn_voz.pack(anchor="center")
        self.btn_tema.pack(anchor="center")
        self.btn_guardar_ajustes.pack(anchor="center")
        # Ventana completa
        self.notebook.pack(fill="both", expand=True)
        self.window.geometry("800x600")
    def cambiar_voz(self):
        if not self.voz_activada:
            self.btn_voz.configure(text="Voz activada")
            self.voz_activada = True
        else:
            self.btn_voz.configure(text="Voz desactivada")
            self.voz_activada = False
    def ajustar_tema_claro(self):
        self.estilo.configure("TNotebook", background="white", borderwidth=0)
        self.estilo.configure("TFrame", background="white", borderwidth=0)
        self.estilo.configure("TLabel", background="white", foreground="black")
        self.estilo.configure("TScale", background="white")
        self.estilo.configure("TButton", padding=(10, 5), background="white")
        self.estilo.configure("TCombobox", padding=(10, 5), background="white")
    def ajustar_tema_oscuro(self):
        self.estilo.configure("TNotebook", background="black", borderwidth=0)
        self.estilo.configure("TFrame", background="black", borderwidth=0)
        self.estilo.configure("TLabel", background="black", foreground="white")
        self.estilo.configure("TScale", background="black")
        self.estilo.configure("TButton", padding=(10, 5), background="black")
        self.estilo.configure("TCombobox", padding=(10, 5), background="black")
    def cambiar_tema(self):
        if not self.tema_oscuro:
            self.btn_tema.configure(text="Tema oscuro")
            self.ajustar_tema_oscuro()
            self.tema_oscuro = True
        else:
            self.btn_tema.configure(text="Tema claro")
            self.ajustar_tema_claro()
            self.tema_oscuro = False
    def decir(self, texto):
        self.tts.say(texto)
        self.tts.runAndWait()
    def enviar_texto(self):
        self.text = self.cuadro_texto.get()
        self.etiqueta_lectura.configure(text=self.text.split()[0])
        self.notebook.select(0)
    def familia_fuente(self, ruta_fuente):
        return ttLib.TTFont(ruta_fuente)['name'].getDebugName(1)
    def pedir_carpeta_fuentes(self):
        carpeta = fd.askdirectory(mustexist=True) + "/"
        if len(os.listdir(carpeta)) < 1:
            return
        self.carpeta_fuentes = carpeta
        self.lista_fuentes = [f.split(".")[0] for f in os.listdir(self.carpeta_fuentes)]
        self.lista_rutas_fuentes = [self.carpeta_fuentes + f for f in os.listdir(self.carpeta_fuentes)]
        self.dict_fuentes = dict(zip(self.lista_fuentes, self.lista_rutas_fuentes))
    def actualizar_ajustes(self):
        if self.selector_fuente.get() == "":
            return
        self.font = Font(root=self.window, file=self.dict_fuentes[self.selector_fuente.get()], family=self.familia_fuente(self.dict_fuentes[self.selector_fuente.get()]), size=self.font_size)
        self.etiqueta_lectura.configure(font=self.font)
        self.etiqueta_prueba.configure(font=self.font)
        self.ajustes["voz"] = self.voz_activada
        self.ajustes["tema-oscuro"] = self.tema_oscuro
        self.ajustes["fuente-selec"] = self.selector_fuente.get()
        self.ajustes["velocidad"] = self.vel
        yaml.safe_dump(self.ajustes, open("assets/config.yaml", "w"), allow_unicode=False)
    def set_speed(self, vel):
        self.vel = round(float(vel))
        self.etiqueta_vel.configure(text="Velocidad (palabras por minuto) - " + str(self.vel))
    def change_label(self):
        self.btn_comenzar.configure(text="Reiniciar")
        if self.index < len(self.lista_palabras):
            self.palabra_actual = self.lista_palabras[self.index]
            self.etiqueta_lectura.configure(text=self.palabra_actual)
            self.index += 1
            if self.vel == 0:
                self.vel = 1
            self.tab1.after(ms=60000//self.vel, func=self.change_label)
    def start_reading(self):
        self.lista_palabras = self.text.split()
        if self.index == 0:
            self.change_label()
        else:
            self.reset_reading()
    def reset_reading(self):
        self.btn_comenzar.configure(text="Iniciar")
        self.index = 0
        self.etiqueta_lectura.configure(text=self.lista_palabras[self.index])
    def cargar_libro(self):
        self.text
        pass
    def run(self):
        self.window.title("FastReading")
        self.window.iconbitmap("assets/icons/logo.ico")
        self.window.mainloop()

app = App()
app.run()