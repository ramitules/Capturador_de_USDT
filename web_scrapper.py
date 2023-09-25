import os
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import exceptions

class web_scrapper(Chrome):
    """
    Clase base para web scrapping con Chrome
    """
    def __init__(self):
        options = self.config_options()
        service = Service()

        super().__init__(options=options, service=service)

    def config_options(self):
        x = os.getcwd()
        o = Options()
        o.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0')
        o.add_argument('--disable-web-security')
        o.add_argument('--disable-notifications')
        o.add_argument('--ignore-certificate-errors')
        o.add_argument('--no-sandbox')
        o.add_argument('--log-level=3')
        o.add_argument('--no-default-browser-check')
        o.add_argument('--no-first-run')
        o.add_argument('--no-proxy-server')
        o.add_argument('--disable-blink-features=AutomationControlled')
        o.add_argument('--headless=new')

        exp_options = ['enable-automation',
                       'ignore-certificate-errors',
                       'enable-logging']

        prefs = {'profile.default_content_setting_values.notifications': 2,
                 'credentials_enable_service': False,
                 'download.default_directory': x}

        o.add_experimental_option('excludeSwitches', exp_options)
        o.add_experimental_option('prefs', prefs)

        return o

    def check_download(self):
        """
        Loop para descargas\n
        Muestra una animacion en la linea de comandos
        """
        ANIMATION_CHARS = ['|', '/', '-', '\\']

        while True:
            for char in ANIMATION_CHARS:
                print(f'\rDownloading  ({char})  ', end='')
                time.sleep(0.15)

            for f in os.listdir():
                if 'crdownload' in f:
                    break

            else:
                print('Download completed')
                return
            
class Binance(web_scrapper):
    """
    Navegador con integracion a la pagina principal de Binance P2P.

    :Args:
        metodo_cobro - seleccionar metodo de cobro preferencial\n
        cantidad - cantidad de pesos a cambiar\n
        verificados - solo mostrar usuarios con verificacion\n
        minimo_ordenes - cantidad de ordenes que tiene que tener el comerciante
    """
    def __init__(
            self,
            metodo_cobro: str | None = None,
            cantidad: float | None = None,
            verificados: bool = False,
            minimo_ordenes: int | None = None,
            filas: int = 3):
        super().__init__()

        self.metodo_cobro = metodo_cobro
        self.cantidad = cantidad
        self.verificados = verificados
        self.minimo_ordenes = minimo_ordenes
        self.filas = filas
        self.xpath_fila = '/html/body/div[1]/div[2]/main/div[1]/div[4]/div/div/div/div[1]/div'

    def buscar_salario(self):
        MAIN_URL = 'https://elsalario.com.ar/Salario/salario-minimo'
        self.get(MAIN_URL)

        texto = self.find_element(By.CLASS_NAME, 'documentDescription.description').text
        texto = texto.split(',')[0].split(' ')[-1].replace('.','').replace('$','')

        self.salario_minimo = texto

        print(f'Salario minimo encontrado: ${self.salario_minimo}')

    def primer_ejecucion(self):
        def wait_full_load():
            while True:
                try:
                    self.find_element(By.XPATH, f'{self.xpath_fila}[5]')
                    return

                except:
                    pass

        print('Trabajando...')
        self.buscar_salario()

        P2P_URL = 'https://p2p.binance.com/es-LA/trade/sell/USDT?fiat=ARS&payment=all-payments'
        self.get(P2P_URL)
        
        wait_full_load()

        print('Configurando Binance P2P...')
        
        xpath_actualizar = '//*[@id="C2CofferList_btn_refresh"]'
        xpath_5seg = '/html/body/div[1]/div[2]/main/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[2]'
        xpath_filtro = '/html/body/div[1]/div[2]/main/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[3]/div'
        xpath_comerciantes = '/html/body/div[1]/div[2]/main/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div[3]/div/div/div/div[1]'

        self.find_element(By.XPATH, xpath_actualizar).click()
        self.find_element(By.XPATH, xpath_5seg).click()
        self.find_element(By.XPATH, xpath_filtro).click()
        self.find_element(By.XPATH, xpath_comerciantes).click()

        wait_full_load()

        print('Completado!')

    def iterar_filas(self):
        anuncios: list[list] = []

        contador = 1

        while (len(anuncios) < self.filas):
            xpath_fila = f'{self.xpath_fila}[{contador}]'

            filas = self.find_element(By.XPATH, xpath_fila)

            contador += 1

            #try:
            anunciante = filas.find_element(By.XPATH, f'{xpath_fila}/div[1]/div[1]/div[1]/a').text
            precio = filas.find_element(By.XPATH, f'{xpath_fila}/div[2]/div[1]/div[1]').text
            minimo = filas.find_element(By.XPATH, f'{xpath_fila}/div[4]/div[2]/div[1]').text.replace('ARS$','').split('.')[0]
            maximo = filas.find_element(By.XPATH, f'{xpath_fila}/div[4]/div[2]/div[3]').text.replace('ARS$','').split('.')[0]
            rango = f"${minimo} - ${maximo}".replace('\n','')
            metodos = filas.find_element(By.XPATH, f'{xpath_fila}/div[5]/div').text.split('\n')
            metodo_pago = ' / '.join(metodos)
            #except: continue

            rango_minimo = int(minimo.replace(',',''))

            if self.metodo_cobro and rango_minimo > int(self.salario_minimo):
                continue

            fila_retorno = [anunciante, precio, rango, metodo_pago]

            anuncios.append(fila_retorno)

        return anuncios