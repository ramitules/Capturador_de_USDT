import threading
import time
from ttkthemes import ThemedTk
from tkinter import ttk, PhotoImage, LEFT
from web_scrapper import Binance

class Mainframe(ThemedTk):
    def __init__(self):
        super().__init__()

        self.title('Capturador de USDT')
        self.geometry('1280x440')

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

        self.boton_ars.pack(pady=10)

    def activar_ars(self):
        self.tabla = self.crear_tabla()

        self.scrapper = Binance(self.frame_ars)
        thread = threading.Thread(target=self.scrapper_loop)
        thread.start()

        self.boton_ars['text'] = 'Detener USDT/ARS'
        self.boton_ars['command'] = self.desactivar_ars

    def desactivar_ars(self):
        for i, widget in enumerate(self.frame_ars.winfo_children()):
            if i == 0:
                continue

            widget.destroy()

        self.scrapper.close()
        del self.scrapper

        self.boton_ars['text'] = 'Activar USDT/ARS'
        self.boton_ars['command'] = self.activar_ars

    def crear_tabla(self):
        tabla = ttk.Treeview(self.frame_ars)

        tabla['columns'] = ('anunciante', 'precio', 'rango', 'metodo')
        tabla['show'] = 'headings'

        tabla.column('anunciante', anchor='center', width=100)
        tabla.column('precio', anchor='center', width=60)
        tabla.column('rango', anchor='center', width=200)
        tabla.column('metodo', anchor='center', width=600)

        tabla.heading('anunciante', text='Anunciante')
        tabla.heading('precio', text='Precio')
        tabla.heading('rango', text='Rango de precios')
        tabla.heading('metodo', text='Metodo de pago')

        tabla.pack(expand=True, fill='both')

        return tabla

    def mostrar_info(self, filas: list):
        self.tabla.delete(*self.tabla.get_children())

        for i, fila in enumerate(filas):
            self.tabla.insert('', i, values=fila)

    def scrapper_loop(self):
        while True:
            anuncios = self.scrapper.iterar_filas()
            self.mostrar_info(anuncios)
            time.sleep(5)

            if self.boton_ars['text'] == 'Activar USDT/ARS':
                break