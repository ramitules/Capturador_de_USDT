from ttkthemes import ThemedTk
from tkinter import ttk, PhotoImage, LEFT
from web_scrapper import Binance

class Mainframe(ThemedTk):
    def __init__(self):
        super().__init__()

        self.title('Capturador de USDT')
        self.geometry('960x440')

        self.load_widgets()
        self.place_widgets()

    def load_widgets(self):
        self.frame_ars = ttk.Frame(self)

        self.boton_ars = ttk.Button(self.frame_ars)

        self.img_ars = PhotoImage(file='media/ars.png')

        self.config_widgets()
        pass

    def config_widgets(self):
        self.boton_ars['text'] = 'Activar USDT/ARS'
        self.boton_ars['command'] = self.activar_ars
        self.boton_ars['compound'] = LEFT
        self.boton_ars['image'] = self.img_ars
        self.boton_ars['padding'] = 4
        
    def place_widgets(self):
        self.frame_ars.pack(expand=True, fill='x')

        self.boton_ars.pack()

    def activar_ars(self):
        #self.tabla = ttk.Treeview(self.frame_ars)
        navegador = Binance(self.frame_ars)
        navegador.mainloop()
        pass
