import threading
import time
from ttkthemes import ThemedTk
from tkinter import ttk, PhotoImage, LEFT
from web_scrapper import Binance

class Mainframe(ThemedTk):
    def __init__(self):
        super().__init__()

        self.title('Capturador de USDT')
        self.geometry('1280x500')

        self.load_widgets()
        self.place_widgets()

    def load_widgets(self):
        #Creacion de widgets
        self.frame_ars = ttk.Frame(self)
        self.args_ars = ttk.Frame(self.frame_ars)

        self.boton_ars = ttk.Button(self.frame_ars)

        self.label_cantidad = ttk.Label(self.args_ars)
        self.label_verif = ttk.Label(self.args_ars)
        self.label_filas = ttk.Label(self.args_ars)
        self.precio_max = ttk.Label(self.frame_ars)
        self.precio_min = ttk.Label(self.frame_ars)

        self.entry_cantidad = ttk.Entry(self.args_ars)
        self.verificados = ttk.Checkbutton(self.args_ars)
        self.entry_filas = ttk.Entry(self.args_ars)

        self.img_ars = PhotoImage(file='media/ars.png')

        self.config_widgets()

    def config_widgets(self):
        #Funcionalidad y seteo de widgets
        self.boton_ars['text'] = 'Activar USDT/ARS'
        self.boton_ars['command'] = self.activar_ars
        self.boton_ars['compound'] = LEFT
        self.boton_ars['image'] = self.img_ars
        self.boton_ars['padding'] = 4

        self.precio_max['justify'] = 'left'
        self.precio_min['justify'] = 'left'

        self.label_cantidad['text'] = 'Cantidad en pesos '
        self.label_verif['text'] = 'Comerciantes verificados '
        self.label_filas['text'] = 'Filas a mostrar '
        
        self.entry_cantidad['validate'] = 'key'
        self.entry_filas['validate'] = 'key'
        
        self.entry_cantidad['validatecommand'] = (self.register(lambda t: t.isdecimal()), '%S')
        self.entry_filas['validatecommand'] = (self.register(lambda t: t.isdecimal()), '%S')

        self.bool_verif = False
        self.verificados['variable'] = self.bool_verif

        self.entry_cantidad.focus()
        
    def place_widgets(self):
        #Acomodar widgets en la pantalla
        self.frame_ars.pack(side='left', padx=20)
        self.args_ars.pack(fill='x', pady=5)

        self.label_cantidad.grid(column=0, row=0, sticky='e')
        self.label_verif.grid(column=0, row=1, sticky='e')
        self.label_filas.grid(column=0, row=2, sticky='e')

        self.entry_cantidad.grid(column=1, row=0, sticky='w')
        self.verificados.grid(column=1, row=1, sticky='w')
        self.entry_filas.grid(column=1, row=2, sticky='w')

        self.boton_ars.pack(pady=5)

        self.precio_max.pack(pady=5, fill='x')
        self.precio_min.pack(pady=5, fill='x')

    def activar_ars(self):
        #Funcion del boton Activar USDT/ARS
        self.crear_tabla()

        self.boton_ars['text'] = 'Desactivar USDT/ARS'
        self.boton_ars['command'] = self.desactivar_ars
        
        #Precios maximos y minimos durante la ejecucion
        self.maximo = 0.0
        self.minimo = 999999.99

        #Parametros web scrapper
        cant = 0
        if self.entry_cantidad.get():
            cant = int(self.entry_cantidad.get())

        filas = 6
        if self.entry_filas.get():
            filas = int(self.entry_filas.get())

        verif = self.bool_verif
        
        #Instanciar un navegador oculto
        self.scrapper = Binance(cantidad=cant, verificados=verif, filas=filas)
        self.scrapper.primer_ejecucion()

        #Delegar la ejecucion a otro hilo
        thread = threading.Thread(target=self.scrapper_loop)
        thread.start()

    def desactivar_ars(self):
        #Limpia pantalla y cierra sesion del navegador
        self.tabla.destroy()

        self.scrapper.close()
        del self.scrapper

        self.boton_ars['text'] = 'Activar USDT/ARS'
        self.boton_ars['command'] = self.activar_ars

    def crear_tabla(self):
        self.tabla = ttk.Treeview(self)

        self.tabla['columns'] = ('anunciante', 'precio', 'rango', 'metodo')
        self.tabla['show'] = 'headings'

        self.tabla.column('anunciante', anchor='center', width=100)
        self.tabla.column('precio', anchor='center', width=60)
        self.tabla.column('rango', anchor='center', width=200)
        self.tabla.column('metodo', anchor='center', width=600)

        self.tabla.heading('anunciante', text='Anunciante')
        self.tabla.heading('precio', text='Precio')
        self.tabla.heading('rango', text='Rango de precios')
        self.tabla.heading('metodo', text='Metodo de pago')

        self.tabla.pack(expand=True, fill='x', side='left')

    def mostrar_info(self, filas: list):
        #Limpia informacion anterior y setea nuevos valores en tabla
        self.tabla.delete(*self.tabla.get_children())

        for i, fila in enumerate(filas):
            self.tabla.insert('', i, values=fila)

            if i > 0:
                continue

            precio = float(fila[1])

            if precio > self.maximo:
                self.maximo = precio
                self.precio_max['text'] = f'Precio maximo: {self.maximo}'

            if precio < self.minimo:
                self.minimo = precio
                self.precio_min['text'] = f'Precio minimo: {self.minimo}'

    def scrapper_loop(self):
        while True:
            anuncios = self.scrapper.iterar_filas()
            self.mostrar_info(anuncios)
            time.sleep(5)

            if self.boton_ars['text'] == 'Activar USDT/ARS':
                break