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
        #Creacion de widgets
        self.frame_ars = ttk.Frame(self)

        self.boton_ars = ttk.Button(self.frame_ars)

        self.referencia = ttk.Label(self.frame_ars)
        self.valor_ref = ttk.Label(self.frame_ars)
        self.precio_max = ttk.Label(self.frame_ars)
        self.precio_min = ttk.Label(self.frame_ars)

        self.img_ars = PhotoImage(file='media/ars.png')

        self.config_widgets()
        pass

    def config_widgets(self):
        #Funcionalidad y seteo de widgets
        self.boton_ars['text'] = 'Activar USDT/ARS'
        self.boton_ars['command'] = self.activar_ars
        self.boton_ars['compound'] = LEFT
        self.boton_ars['image'] = self.img_ars
        self.boton_ars['padding'] = 4

        self.referencia['justify'] = 'left'
        self.valor_ref['justify'] = 'center'
        self.precio_max['justify'] = 'left'
        self.precio_min['justify'] = 'left'

        
        
    def place_widgets(self):
        #Acomodar widgets en la pantalla
        self.frame_ars.pack(side='left', padx=20)
        self.boton_ars.pack(pady=5)

        self.referencia.pack(pady=5, fill='x')
        self.valor_ref.pack(pady=5)
        self.precio_max.pack(pady=5, fill='x')
        self.precio_min.pack(pady=5, fill='x')

    def activar_ars(self):
        #Funcion del boton Activar USDT/ARS
        self.tabla = self.crear_tabla()

        self.referencia['text'] = 'Rango minimo = salario minimo'

        self.boton_ars['text'] = 'Desactivar USDT/ARS'
        self.boton_ars['command'] = self.desactivar_ars
        
        #Precios maximos y minimos durante la ejecucion
        self.maximo = 0.0
        self.minimo = 999999.99

        #Instanciar un navegador oculto
        self.scrapper = Binance(filas=6)
        self.scrapper.primer_ejecucion()

        #Delegar la ejecucion a otro hilo
        thread = threading.Thread(target=self.scrapper_loop)
        thread.start()

        self.valor_ref['text'] = f'$ {self.scrapper.salario_minimo}'

    def desactivar_ars(self):
        #Limpia pantalla y cierra sesion del navegador
        for i, widget in enumerate(self.frame_ars.winfo_children()):
            if i < 3:
                continue

            widget.destroy()

        self.scrapper.close()
        del self.scrapper

        self.boton_ars['text'] = 'Activar USDT/ARS'
        self.boton_ars['command'] = self.activar_ars

    def crear_tabla(self):
        tabla = ttk.Treeview(self)

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

        tabla.pack(expand=True, fill='x', side='left')

        return tabla

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