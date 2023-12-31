import tkinter as tk
from tkinter import ttk
from tkextrafont import Font

t = open("text.txt", "r", encoding="utf-8")

class WordByWordTextDisplay:
    def __init__(self, text: str):
        self.root = tk.Tk()
        self.font_size = 72
        self.font = Font(file="assets/fonts/OpenDyslexic.otf", family="OpenDyslexic", size=self.font_size)
        self.root.iconbitmap("assets/icons/logo.ico")
        self.root.title("FastReading")
        self.text = text.split()
        self.speed = 15  # La velocidad predeterminada es 15 palabras por minuto
        self.index = 0

        self.word_label = tk.Label(self.root, text="", font=self.font, anchor="center")
        self.word_label.pack(expand=True, fill="both")
        self.root.update()

        self.speed_slider = tk.Scale(self.root, from_=5, to=250, resolution=5, orient=tk.HORIZONTAL, length=200, label="Velocidad (palabras por minuto)", command=self.set_speed)
        self.speed_slider.set(5)
        self.speed_slider.pack()

        self.start_button = tk.Button(self.root, text="Comenzar", command=self.start_display, width=25)
        self.start_button.configure(relief="groove")
        self.start_button.pack()

        self.restart_button = tk.Button(self.root, text="Reiniciar", command=self.restart_display, width=25)
        self.restart_button.configure(relief="groove")
        self.restart_button.pack()

        self.pause_button = tk.Button(self.root, text="Pausar", command=self.pause_display, width=25)
        self.pause_button.configure(relief="groove")
        self.pause_button.pack()

        self.root.state('zoomed')
        self.root.geometry(f"+{self.root.winfo_screenwidth()//2}+{self.root.winfo_screenheight()//2}")

    def start_display(self):
        self.speed = self.speed_slider.get()
        self.word_label.configure(text=self.text[self.index])
        self.index += 1
        if self.index < len(self.text):
            self.root.after(ms=60000//self.speed, func=self.start_display)

    def restart_display(self):
        self.index = 0
        self.start_display()

    def pause_display(self):
        self.speed = 0
        self.word_label.configure(text=self.text[self.index])

    def set_speed(self, speed):
        self.speed = float(speed)

    def run(self):
        self.root.mainloop()


# Ejemplo de uso
text = t.read()
display = WordByWordTextDisplay(text)
display.run()
