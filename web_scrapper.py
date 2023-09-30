import os
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
                       'ignore-certificate-errors']

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
            cantidad: int,
            verificados: bool,
            filas: int):
        super().__init__()

        self.cantidad = cantidad
        self.verificados = verificados
        self.filas = filas
        self.xpath_fila = '//*[@id="__APP"]/div[2]/main/div[1]/div[4]/div/div/div/div[1]/div'

    def wait_full_load(self):
        while True:
            try:
                self.find_element(By.XPATH, f'{self.xpath_fila}[5]')
                return

            except:
                pass

    def primer_ejecucion(self):
        print('Trabajando...')

        P2P_URL = 'https://p2p.binance.com/es-LA/trade/sell/USDT?fiat=ARS&payment=all-payments'
        self.get(P2P_URL)
        
        self.wait_full_load()

        print('Configurando Binance P2P...')
        
        #Actualizar cada 5 segundos
        xpath_actualizar = '//*[@id="C2CofferList_btn_refresh"]'
        self.find_element(By.XPATH, xpath_actualizar).click()

        xpath_5seg = '//*[@id="__APP"]/div[2]/main/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[2]'
        self.find_element(By.XPATH, xpath_5seg).click()

        #Cantidad
        if self.cantidad:
            xpath_cantidad = '//*[@id="C2Csearchamount_searchbox_amount"]'
            self.find_element(By.XPATH, xpath_cantidad).send_keys(str(self.cantidad))

        #Comerciantes verificados
        if self.verificados:
            xpath_filtro = '/html/body/div[1]/div[2]/main/div[1]/div[3]/div[2]/div/div/div[2]/button'
            self.find_element(By.XPATH, xpath_filtro).click()

            xpath_comerciantes = '/html/body/div[9]/div[1]/div/div/div[2]/div/div[2]/label/div[1]'
            self.find_element(By.XPATH, xpath_comerciantes).click()

            xpath_confirmar_verif = '/html/body/div[9]/div[1]/div/div/div[2]/div/div[4]/button[2]'
            self.find_element(By.XPATH, xpath_confirmar_verif).click()

        self.wait_full_load()

        print('Completado!')

    def iterar_filas(self):
        self.wait_full_load()

        time.sleep(1)

        anuncios: list[list] = []

        contador = 1

        while (len(anuncios) < self.filas):
            xpath_fila = f'{self.xpath_fila}[{contador}]'

            filas = self.find_element(By.XPATH, xpath_fila)

            contador += 1

            anunciante = filas.find_element(By.XPATH, f'{xpath_fila}/div[1]/div[1]/div[1]/a').text
            precio = filas.find_element(By.XPATH, f'{xpath_fila}/div[2]/div[1]/div[1]').text
            minimo = filas.find_element(By.XPATH, f'{xpath_fila}/div[4]/div[2]/div[1]').text.replace('ARS$','').split('.')[0]
            maximo = filas.find_element(By.XPATH, f'{xpath_fila}/div[4]/div[2]/div[3]').text.replace('ARS$','').split('.')[0]
            rango = f"${minimo} - ${maximo}".replace('\n','')
            metodos = filas.find_element(By.XPATH, f'{xpath_fila}/div[5]/div').text.split('\n')
            metodo_pago = ' / '.join(metodos)

            fila_retorno = [anunciante, precio, rango, metodo_pago]

            anuncios.append(fila_retorno)

        return anuncios