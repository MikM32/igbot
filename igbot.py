"""
    Bot para Instagram
    Autor: Miguel Matute
    Fecha: 05/01/2024

    Descripcion:
        -este bot usa la api de selenium para las interacciones con los diferentes elementos de las paginas y para web scrapping
    Notas del autor:
        -durante todas las pruebas, instagram no ha detectado actividad sospechosa. Pero esto no quiere decir que no pueda detectarla.
        -El uso prolongado del bot puede levantar sospechas por parte de instagram, cosa que no me ha pasado hasta ahora por suerte.
        -Opte por ocultar la ventana del navegador con la api de windows como alternativa al modo headless de chrome que es muy peligroso.
"""

import time
import os, sys
import secrets

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.firefox.service import Service as FService

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from win32gui import GetWindowText
from win32gui import EnumWindows
from win32gui import ShowWindow
from win32gui import SetForegroundWindow

from faker import Faker

import default_browser
import data

from bot_exceptions import *
from constants import *

def get_webdriver_path(browser_type: str) -> str:
    """
    funcion que retorna la ruta del ejecutable del webdriver segun el tipo de navegador especificado en los parametros
    """

    webdriver_path= WEBDRIVER_ROOT_PATH

    if "Chrome" in browser_type:
        version = default_browser.get_chrome_version()
        cur_os = sys.platform
        webdriver_path+= f".wdm/drivers/chromedriver/{cur_os}/{version}/chromedriver-{cur_os}/chromedriver.exe"
    #elif "Firefox" in browser_type:
    #    webdriver_path+= "geckodriver.exe"
    else:
        raise UncompatibleDefaultBrowser(browser_type)

    return webdriver_path

def display_window(wintitle:str, display:bool):
    """
        Funcion que oculta o muestra una ventana especificada por su titulo
    """

    hide_callback = lambda hwnd, lparam: ShowWindow(hwnd, 0) if wintitle in GetWindowText(hwnd) else None
    show_callback = lambda hwnd, lparam: ShowWindow(hwnd, 5) if wintitle in GetWindowText(hwnd) else None

    if display:
        EnumWindows(show_callback, 0)
    else:
        EnumWindows(hide_callback, 0)

def set_active_window(wintitle: str):

    active_callback = lambda hwnd, lparam: SetForegroundWindow(hwnd) if wintitle in GetWindowText(hwnd) else None
    EnumWindows(active_callback, 0)

def clean_name(name:str) -> str:

    accents = {' ':'','ñ':'n' ,'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    res = name
    for accent in accents.keys():
        res = res.replace(accent, accents[accent])
    return res

def gen_birth() -> str:

    faker = Faker(['es_MX'])
    date = faker.date_of_birth(minimum_age=19, maximum_age=30)
    

    return f'{str(date.day)}/{str(date.month)}/{str(date.year)}'

def gen_name() -> str:
    faker = Faker(['es_MX'])

    return clean_name(faker.first_name())

def gen_email() -> str:
    faker = Faker(['es_MX'])

    return chr(secrets.randbelow(20)+97) + clean_name(faker.last_name().lower()) + str(secrets.randbelow(200))

def gen_pwd() -> str:
    #faker = Faker(['es_MX'])

    return secrets.token_hex(8)

get_element = lambda bhandler, locator: WebDriverWait(bhandler, WAIT_MAX).until(EC.presence_of_element_located(locator))
"""
    funcion que espera 60 segundos a que un elemento cargue y luego lo retorna
"""
get_elements = lambda bhandler, locator: WebDriverWait(bhandler, WAIT_MAX).until(EC.presence_of_all_elements_located(locator))
"""
    funcion que espera 60 segundos a que todos los elementos especificador por el locator esten cargados luego devuelve la lista de los elementos
"""

get_clickable_element = lambda bhandler, locator: WebDriverWait(bhandler, WAIT_MAX).until(EC.element_to_be_clickable(locator))

#<------------------------------><------------------------------><------------------------------>
class Browser:
    """
        Clase Browser:

        -- atributos:
            -browser_handler: handler del navegador

            -def_browser: cadena que contiene el directorio donde se encuentra el ejecutable del navegador predeterminado

            -options: objeto que contiene los parametros con los cual arrancara el navegador

            -service: objeto que contiene la informacion del webdriver que sera utilizado por el browser_handler

            -sleep_secs: entero que contiene la cantidad de segundos que usara la funcion Browser.wait() para esperar

        -- Metodos:

            -init_browser_handler()

            -save_cookies(pre: str)

            -load_cookies(pre: str)

            -delete_cookies()

            -wait()

            -close_browser_handler()
    """
    def __init__(self,
                 browser_path: str='',
                 custom_b_handler: webdriver.Chrome = None,
                 use_vpn: bool = False,
                 headless: bool = False):

        self.webdriver_path = None
        self.def_browser = None
        self.is_headless = headless
        self.use_vpn = use_vpn
        self.is_active_vpn = False
        self.__is_hide = False
        self.__first_run = False

        if(not browser_path):
             self.def_browser = default_browser.get_browser_exepath()
        else:
            self.def_browser = browser_path
        self.webdriver_path = get_webdriver_path(self.def_browser)

        self.browser_handler = custom_b_handler
        self.options = None
        self.service = None
        self.sleep_secs = None

    def _patch_chromedriver(self):
        """
            Reemplaza la JSfingerprint del webdriver para evitar detecciones
        """

        data = None
        old_fingerprint = None

        if(os.path.exists(PATCH_INFO_PATH)):
            with open(PATCH_INFO_PATH, 'r') as fso:
                old_fingerprint = fso.read()
        else:
            old_fingerprint = 'cdc_'


        with open(self.webdriver_path, 'rb') as fso:
            data = fso.read()

        new_fingerprint = secrets.choice(['lll', 'AaA', 'oAo', 'kol', 'Akr', 'PlP', 'mel', 'yes', 'nop', 'ghi', 'cgi'])
        new_fingerprint+= '_'

        data = data.replace(bytes(old_fingerprint, 'ansi'), bytes(new_fingerprint, 'ansi'))

        with open(self.webdriver_path, 'wb') as fso:
            fso.write(data)
        del data

        with open(PATCH_INFO_PATH, 'w') as fso:
            fso.write(new_fingerprint)


    def _init_chrome(self):
        self.options = COptions()
        #full_userdata_path = os.path.join(os.getcwd(), CHROME_USER_DATA)
        #self.options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
        #if self.is_headless:
            #ejecuta el programa sin la ventana del navegador
        ###    self.options.add_argument('--headless=new') #No te recomendaria decomentar esta seccion XD
        #    self.options.add_experimental_option('prefs', {'intl.accept_languages': 'es,es_ES'})
        if self.use_vpn:
            full_path = os.path.join(os.getcwd(), URBAN_VPN_EXT_PATH)
            self.options.add_argument(f'--load-extension={full_path}')
        #full_profile_path = os.path.join(os.getcwd(), PROFILE_PATH)

        #user_path = os.environ['userprofile']
        #if self._check_profile_exists(user_path, 'IgbotData'):
        random_user_agent = secrets.choice(USER_AGENTS)
        self.options.add_argument(f"--user-agent={random_user_agent}")
        self.options.add_argument(f'--profile-directory=Default')
        #else:
        #    self.options.add_argument(f'--args')
        #    self.options.add_argument(f'--profile-directory="IgbotData"')
        #    self.options.add_argument(f'--first-run')
        #    self.__first_run = True

        #Este parametro evita que aparezca el mensaje "Un software automatizado esta controlando chrome"
        self.options.add_experimental_option('excludeSwitches', ["enable-automation"])

        #Este parametro permite que la ventana del navegador permanezca abierta aun despues de haber realizado alguna tarea.
        self.options.add_experimental_option('detach', True)

        self.options.binary_location = self.def_browser
        self.service = None

        #Descarga los chromedrivers necesarios si no se detectan en WEBDRIVER_ROOT_PATH
        if(not os.path.exists(self.webdriver_path)):
            cache_manager = DriverCacheManager(WEBDRIVER_ROOT_PATH) #Especifica la ruta de descarga e instalacion del webdriver
            current_version = default_browser.get_chrome_version()
            warning('Actualizando webdriver...')
            self.service = CService(ChromeDriverManager(driver_version=current_version, cache_manager=cache_manager).install())

        else:
            self._patch_chromedriver()
            self.service = CService(executable_path=self.webdriver_path)
        self.browser_handler = webdriver.Chrome(options=self.options, service=self.service)

    #Comentado porque firefox perdio soporte
    #def _init_firefox(self):
    #    self.options = FOptions()
    #    self.options.binary = self.def_browser
    #    self.service = FService(executable_path=self.webdriver_path)
    #    self.browser_handler = webdriver.Firefox(options=self.options, service=self.service)
    def _check_profile_exists(self, user_path:str, profile:str) ->bool:

        chrome_data = user_path + CHROME_DATA_PATH + profile
        if not os.path.exists(chrome_data):
            return False
        return True

    def hide_window(self, inital_page: bool=False):
        if not self.__is_hide:
            try:
                title= ''
                if inital_page:
                    title = 'data:,'
                else:
                    title = self.browser_handler.title
                display_window(title, False)
                self.__is_hide = True
            except Exception as e:
                warning(f'No se pudo ocultar la ventana: {e}')

    def show_window(self):
        if self.__is_hide:
            try:
                display_window(self.browser_handler.title, True)
                self.__is_hide = False
            except Exception as e:
                warning(f'No se pudo mostrar la ventana: {e}')
    
    def active_window(self):

        try:
            set_active_window(self.browser_handler.title)
        except Exception as e:
            warning(f'No se pudo activar la ventana: {e}')
    # def _install_vpn_ext(self):
    #     self.browser_handler.get(WEBSTORE_VPN_LINK)

    #     locator = (By.CLASS_NAME, INSTALL_BT)
    #     install_button = get_element(self.browser_handler, locator)
    #     install_button.click()

    def init_browser_handler(self):
        """"
            Inicializa el webdriver
        """
        if self.browser_handler is not None:
            return

        if "Chrome" in self.def_browser:
            self._init_chrome()

            #if self.__first_run:
            #    ok_button = get_element(self.browser_handler, (By.ID, OK_BT_ID))
            #    ok_button.click()
            #    self._install_vpn_ext()

        #!!IMPORTANTE!!: Firefox perdera soporte por falta de metodos para evadir la deteccion de bots.
        #elif "Firefox" in self.def_browser:
        #    self._init_firefox()
        else:
            raise UncompatibleDefaultBrowser(self.def_browser)


    def save_cookies(self, webname: str, username: str):
        """
            metodo que guarda las cookies de sesion del usuario actual en la base de datos.
            El formato de los nombres en el campo Usuarios de la base de datos es: NOMBRE_DE_WEB+_+USERNAME.

             Por ejemplo: para un usuario de instagram seria webname = 'instagram', username= 'fulano123.'
             y por lo tanto se guardaria en la base de datos como instagram_fulano123.
        """

        cookies = self.browser_handler.get_cookies()

        #with open(COOKIES_PATH+pre+'_cookies.json', 'w+') as file_cookie:
        #    json.dump(cookies, file_cookie)

        data.db_save_cookies(COOKIES_DB, webname, username, cookies)

    def delete_cookies(self):
        self.browser_handler.delete_all_cookies()

    def load_cookies(self, webname: str, username: str):
        """
            Carga las cookies de sesion de una red social determinada
            por el parametro webname y el nombre de usuario, el cual es una cadena que contiene
            el prefijo de la red social. Ejem: instagram, facebook,
            tiktok, etc...
        """
        try:
            #with open(COOKIES_PATH+pre+'_cookies.json', 'r') as file_cookie:
            #    cookies = json.load(file_cookie)

            cookies = data.db_load_cookies(COOKIES_DB, webname, username)

            self.browser_handler.execute_cdp_cmd('Network.enable',{})

            for cookie in cookies:
                self.browser_handler.execute_cdp_cmd('Network.setCookie', cookie)
            self.refresh()

            self.browser_handler.execute_cdp_cmd('Network.disable', {})
        except FileNotFoundError:
            raise CookiesDontExists(username)

    def refresh(self):
        if not self.browser_handler:
            raise NotInitizalizedHandler()
        self.browser_handler.refresh()

    def wait(self, type: str=''):
        """
            Metodo que hace esperar al navegador unos segundos
            (Dificulta la deteccion del bot)
            type: parametro que representa la forma en la que se refrescan los segundos de espera (tiempo de espera normal, small, micro, nano y search)
        """
        int_interval = 2
        int_offset = 0
        float_interval = 9

        if not type:
            int_offset = 4
        elif 'small' in type:
            int_offset = 2
        elif 'micro' in type:
            int_interval = 1
            int_offset = 1
            float_interval = 5
        elif 'nano' in type:
            int_interval = 1
            int_offset = 0.2
            float_interval = 2
        elif 'search' in type:
            time.sleep(1.5)
            return
        else:
            raise WaitTypeException(type)

        self._update_sleep_secs(float_interval, int_interval, int_offset)
        time.sleep(self.sleep_secs)

    def _update_sleep_secs(self, float_interval: int, int_interval: int, int_offset: int):
        float_part = secrets.randbelow(float_interval) / 10
        int_part = secrets.randbelow(int_interval) + int_offset
        self.sleep_secs = int_part + float_part

    def close_browser_handler(self):

        if(not self.browser_handler): #self.browser_handler == None
            raise NotInitizalizedHandler()

        self.browser_handler.quit()

#<------------------------------><------------------------------><------------------------------>
class UrbanVpn(Browser):

    def __init__(self,
                 browser_path: str='',
                 custom_b_handler: webdriver.Chrome = None,
                 use_vpn: bool = True,
                 headless: bool = False
                 #country: str,
                 #ad_block: bool,
                 #anti_phish: bool
                 ):

        super().__init__(browser_path, custom_b_handler, use_vpn, headless)
        #self.country = country
        #self.ad_block = ad_block
        #self.anti_phish = anti_phish

        self.__is_in_page = False
        self.__is_active = False
        self.__first_use = True
        self.whandle = ''


    def init_page(self):

        self.browser_handler.switch_to.new_window('vpnw')
        self.browser_handler.implicitly_wait(4)
        self.browser_handler.get(URBAN_VPN_LINK)
        self.__is_in_page = True

        if not self.__first_use:
            return
        WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.number_of_windows_to_be(3))
        current_handle = self.browser_handler.current_window_handle
        self.whandle = current_handle

        for handle in self.browser_handler.window_handles[::-1]:
            if handle != current_handle:
                self.browser_handler.switch_to.window(handle)
                self.browser_handler.close()
                break
                # try:
                #     WebDriverWait(self.browser_handler, 3).until(EC.title_is('VPN for Desktop - Maximum Security & Browsing | UrbanVPN'))
                #     self.browser_handler.close()
                # except:
                #     pass

        self.browser_handler.switch_to.window(current_handle)
        self.accept_terms()
        self.__first_use = False


    def accept_terms(self):
        if not self.__is_in_page:
            raise PageNotLoaded(URBAN_VPN_LINK)
        #WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located((By.CLASS_NAME, 'promotion__text')))
        get_element(self.browser_handler, (By.CLASS_NAME, 'promotion__text'))

        try:
            #terms_button = self.browser_handler.find_element(By.CLASS_NAME, 'consent-text-controls__action')
            terms_button = get_element(self.browser_handler, (By.CLASS_NAME, 'consent-text-controls__action'))
            terms_button.click()
            self.wait('nano')

            #self.browser.save_cookies('vpn')
        except NoSuchElementException:
            #warning('no cargo la pagina para aceptar terminos')
            pass


    def activate(self):

        if self.__is_active:
            return
        elif not self.__is_in_page:
            raise PageNotLoaded(URBAN_VPN_LINK)

        try:
            c_locator = (By.CSS_SELECTOR, f'li[class="{LOCATION_ITEM_CLASS}"]')
            s_locator = (By.CSS_SELECTOR, f'div[class="{SELECTION_INPUT_CLASSES}"]')
            b_locator = (By.CSS_SELECTOR, f'div[class="{SELECTION_BOX_CLASSES}"]')
            #selection_input =  WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(s_locator))
            selection_input = get_element(self.browser_handler, s_locator)
            selection_input.click()
            #selection_box = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(b_locator))
            selection_box = get_element(self.browser_handler, b_locator)
            #countries_list =  WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_all_elements_located(c_locator))
            countries_list = get_elements(self.browser_handler, c_locator)

            curelement = None
            country = secrets.choice(['United States (USA)','Canada']) #'Australia', 'Canada', 'United Kingdom', ])
            for element in countries_list:
                self.browser_handler.execute_script("arguments[0].scrollIntoView();", element)
                #print(element.text)
                if country in element.text:
                    curelement = element
                    break
            #index = secrets.randbelow(len(countries_list))
            #self.browser_handler.execute_script("arguments[0].scrollIntoView();", curelement)#countries_list[index])
            #countries_list[index].click()
            curelement.click()

            #run_button = self.browser_handler.find_element(By.CLASS_NAME, 'play-button--play')
            #run_button.click()

            #WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located((By.CLASS_NAME, 'play-button--pause')))
            get_element(self.browser_handler, (By.CLASS_NAME, 'play-button--pause'))
            locator = (By.CLASS_NAME, 'loader loader--animated primary-layout__loader')
            WebDriverWait(self.browser_handler, WAIT_MAX).until_not(EC.presence_of_element_located(locator))
            self.__is_active = True
            self.wait('micro')
            #print('listo')
        except TimeoutException as e:
            warning('No se encontraron elementos necesarios para activar el vpn')
            warning(repr(e))

    def deactivate(self):
        if not self.__is_active:
            return
        elif not self.__is_in_page:
            raise PageNotLoaded(URBAN_VPN_LINK)

        self.wait('nano')
        #stop_button = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located((By.CLASS_NAME, 'play-button--pause')))
        stop_button = get_element(self.browser_handler, (By.CLASS_NAME, 'play-button--pause'))
        stop_button.click()
        self.__is_active = False
        self.wait('nano')

    def switch_to_vpn(self):

        self.browser_handler.switch_to.window(self.whandle)

    def close(self):
        self.__is_in_page = False
        self.browser_handler.close()


#<------------------------------><------------------------------><------------------------------>
class ProtonMail(Browser):

    def __init__(self,
                 username:str='',
                 pwd:str='',
                 browser_path: str='',
                 custom_b_handler: webdriver.Chrome = None,
                 use_vpn: bool = False,
                 headless: bool = False
                 ):

        self.username = username
        self.pwd = pwd
        self.vpn = None
        self.whandle = ''

        super().__init__(browser_path, custom_b_handler, use_vpn, headless)

    def _init_vpn(self):
        self.vpn = UrbanVpn(custom_b_handler=self.browser_handler)
        prev_handle = self.browser_handler.current_window_handle
        self.vpn.init_page()
        self.browser_handler.switch_to.window(prev_handle)
        self.is_active_vpn = True


    def activate_vpn(self):
        if not self.vpn:
            raise IgBotNotInitializedVpn()
        if self.is_active_vpn:
            return
        prev_handle = self.browser_handler.current_window_handle
        self.vpn.switch_to_vpn()
        self.vpn.activate()
        self.browser_handler.switch_to.window(prev_handle)

    def deactivate_vpn(self):
        if not self.vpn:
            raise IgBotNotInitializedVpn()
        if not self.is_active_vpn:
            return
        prev_handle = self.browser_handler.current_window_handle
        self.vpn.switch_to_vpn()
        self.vpn.deactivate()
        self.browser_handler.switch_to.window(prev_handle)

    def init_web(self):
        if self.use_vpn:
            if not self.is_active_vpn:
                self._init_vpn()

    def create_new_account(self) -> tuple[str]:
        
        return self.register(gen_email(), gen_pwd())
                             
    def register(self, email:str, pwd:str ) -> tuple[str]:
        self.whandle = self.browser_handler.current_window_handle
        if self.use_vpn:
            if not self.is_active_vpn:
                self.activate_vpn()
        self.browser_handler.get(PROTONMAIL_REG_URL)

        # locator = (By.CSS_SELECTOR, f'input[class="{PREG_EMAIL_INPUT_ID}"]:nth-child(2)')
        # email_input = get_element(self.browser_handler, locator)

        # locator = (By.CSS_SELECTOR, f'input[id="{PREG_PWD_INPUT_ID}"]')
        # pwd_input = get_element(self.browser_handler, locator)

        # locator = (By.CSS_SELECTOR, f'input[id="{PREG_CONFIRM_PWD_ID}"]')
        # confirm_pwd_input = get_element(self.browser_handler, locator)

        # email_input.send_keys(email)
        # pwd_input.send_keys(pwd)
        # confirm_pwd_input.send_keys(pwd)

        locator = (By.CSS_SELECTOR, 'iframe[title="Nombre de usuario"]')
        iframe = get_element(self.browser_handler, locator)

        self.browser_handler.switch_to.frame(iframe)

        user_input =  self.browser_handler.find_element(By.ID, 'email')

        user_input.send_keys(email)

        self.browser_handler.switch_to.default_content()

        locator = (By.ID, PREG_PWD_INPUT_ID)
        pwd_input = get_element(self.browser_handler, locator)

        pwd_input.send_keys(pwd)
        self.wait('micro')

        locator = (By.ID, PREG_CONFIRM_PWD_ID)
        pwd_conf_input = get_element(self.browser_handler, locator)

        pwd_conf_input.send_keys(pwd)
        self.wait('nano')

        locator = (By.CSS_SELECTOR, f'button[type="submit"]')
        submit_bt = get_element(self.browser_handler, locator)

        submit_bt.click()


        #resolver captcha
        locator = (By.XPATH, "//h1[contains(text(), 'Verifica')]")
        get_element(self.browser_handler, locator)
        while True:
            try:
                 self.browser_handler.find_element(By.XPATH, "//span[contains(text(), 'CAPTCHA')]")
                 self.wait('micro')
            except:
                 print('listo')
                 break
        
        self.wait('nano')

        try:
            locator = (By.CSS_SELECTOR, f'button[class="{PNAME_NEXT}"]')
            next_bt2 = get_element(self.browser_handler, locator)
            next_bt2.click()

            self.wait('micro')

            locator = (By.XPATH, "//button[contains(text(), 'tarde')]")
            omit_bt = get_element(self.browser_handler, locator)
            omit_bt.click()

            self.wait('micro')

            locator = (By.XPATH, "//button[contains(text(), 'Confirmar')]")
            omit_bt = get_element(self.browser_handler, locator)
            omit_bt.click()

            self.wait('micro')
            locator = (By.XPATH, "//button[contains(text(), 'Siguiente')]")
            omit_bt = get_element(self.browser_handler, locator)
            omit_bt.click()

            #locator = (By.XPATH, "//button[contains(text(), 'siguiente')]")
            #omit_bt = get_element(self.browser_handler, locator)
            omit_bt.click()

            self.wait('micro')

            locator = (By.XPATH, "//button[contains(text(), 'Omitir')]")
            omit_bt = get_element(self.browser_handler, locator)
            omit_bt.click()
        except TimeoutException as e:
            warning('algunos elementos no se pudieron cargar')
            warning(repr(e))
        
        return email, pwd

        #omitir datos de recuperacion

        #omitir introduccion

        #listo

    def login(self):
        pass

    def get_mail_subject(self, mail_kword: str) -> str:
        
        #self.active_window()
        self.wait()
        try:
            locator = (By.CSS_SELECTOR, 'svg[data-testid="navigation-link:refresh-folder"]')
            refresh_bt = get_element(self.browser_handler, locator)
            self.wait('micro')
            refresh_bt.click()

            locator = (By.CSS_SELECTOR, 'span[role="heading"]')
            subjects = get_elements(self.browser_handler, locator)

            for subject in subjects:
                if mail_kword in subject.text:
                    return subject.text
        except Exception as e:
            warning(f'No se encontraron elementos necesarios para poder leer el correo: {e}')
        
        return None

    def close(self):
        if self.use_vpn:
            prev_handle = self.browser_handler.current_window_handle
            self.vpn.switch_to_vpn()
            self.vpn.deactivate()
            self.vpn.close()
            self.browser_handler.switch_to.window(prev_handle)

        self.close_browser_handler()


#<------------------------------><------------------------------><------------------------------>
class IgBot(Browser):
    """
        Clase IgBot:

            --Propiedades:

                -username: nombre de usuario de la cuenta con la que se esta trabajando

                -is_logged: booleano que determina si la sesion ya esta iniciada

            --Metodos:

                * __init__(*args):
                    args contiene un parametro opcional que seria la ruta del webdriver especificada por el usuario

                * init_ig():
                    carga la pagina principal de instagram

                * login(user: str, pwd: str):
                    inicia sesion con una cuenta en instagram
    """
    def __init__(self,
                 username: str='',
                 pwd: str='',
                 browser_path: str ='',
                 custom_b_handler: webdriver.Chrome = None,
                 use_vpn: bool = False,
                 headless:bool = False):

        self.username = username
        self.pwd = pwd
        self.vpn = None
        self.is_logged = False
        self.__is_in_page = False

        super().__init__(browser_path, custom_b_handler, use_vpn, headless)

        self._init_paths()
        self._init_db('instagram')

    def _init_paths(self):
        if(not os.path.exists(COOKIES_PATH)):
            os.mkdir(COOKIES_PATH)

    def _init_db(self, webname: str):

        data.db_init(COOKIES_DB, webname)

    def _init_vpn(self):
        self.vpn = UrbanVpn(custom_b_handler=self.browser_handler)
        prev_handle = self.browser_handler.current_window_handle
        self.vpn.init_page()
        self.browser_handler.switch_to.window(prev_handle)
        self.is_active_vpn = True

        #self.wait('nano')

    def set_username(self, usr: str):
        self.username = usr

    def set_pwd(self, pwd: str):
        self.pwd = pwd

    def activate_vpn(self):

        if not self.use_vpn:
            raise IgBotNotInitializedVpn()
        prev_handle = self.browser_handler.current_window_handle
        self.vpn.switch_to_vpn()
        self.vpn.activate()
        self.browser_handler.switch_to.window(prev_handle)

    def deactivate_vpn(self):

        if not self.use_vpn:
            raise IgBotNotInitializedVpn()
        prev_handle = self.browser_handler.current_window_handle
        self.vpn.switch_to_vpn()
        self.vpn.deactivate()
        self.browser_handler.switch_to.window(prev_handle)

    def init_ig(self, preload_cookies:bool = True):
        """
            Metodo que inicializa el browser_handler(webdriver), vpn, carga las cookies de sesion e inicia la pagina principal de instagram
        """
        self.init_browser_handler()
        if self.is_headless:
            self.hide_window(inital_page=True)
        if self.use_vpn:
            self._init_vpn()
            self.activate_vpn()

        self.browser_handler.implicitly_wait(5)
        if preload_cookies:
            if self.username:
                try:
                    self.load_cookies('instagram', self.username)
                    self.is_logged = True
                except CookiesDontExists as e:
                    warning(f'Error al cargar cookies de sesion para {self.username}: {e}')
                    self.is_logged = False
            else:
                warning(IgUsernameNotFound().msg)
                #raise IgUsernameNotFound()

        self.browser_handler.get(IG_URL)
        #Si aparece el popup preguntando si se desea aceptar cookies del sitio le de a aceptar
        try:
            self.wait('micro')
            accept_bt = self.browser_handler.find_element(By.CSS_SELECTOR, 'button[class="_a9-- _ap36 _a9_0"]')
            accept_bt.click()
        except:
            pass
        self.whandle = self.browser_handler.current_window_handle
        self.__is_in_page = True

        #if not self.is_logged:
        #    self.login(True, False)

    def accept_notifications(self, accept: bool):
        """
            da click en aceptar o rechazar en la ventana emergente de notificaciones dependiendo del parametro accept
        """
        self._check_login('No se puede ejecutar el metodo: accept_notifications()')

        self.wait('micro')
        try:

            locator = (By.CSS_SELECTOR, 'div[class="_a9-y"]')
            msg_span = get_element(self.browser_handler, locator)
            self.browser_handler.execute_script('arguments[0].click();', msg_span)
            locator = (By.CSS_SELECTOR, f'button[class="{ACCEPT_NOTIFICATIONS_SL}"]')
            #accept_button = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            #accept_button = get_element(self.browser_handler, locator)
            accept_button = get_clickable_element(self.browser_handler, locator)

            locator = (By.CSS_SELECTOR, f'button[class="{DONT_ACCEPT_NOTIFICATIONS_SL}"]')
            #no_accept_button = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            no_accept_button = get_clickable_element(self.browser_handler, locator)
            #accept_button = self.browser_handler.find_element(By.CSS_SELECTOR, ACCEPT_NOTIFICATIONS_SL)
            #no_accept_button = self.browser_handler.find_element(By.CSS_SELECTOR, DONT_ACCEPT_NOTIFICATIONS_SL)

            if accept:
                accept_button.click()
            else:
                no_accept_button.click()

            #self.save_cookies('instagram', self.username)
        except Exception:
            warning("No se encuentra la ventana de notificaciones.")
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.accept_notifications(accept)

    def accept_session_cookies(self, save: bool):
        """
            si se inicia sesion con datos (password y username), acepta o rechaza el uso de cookies de sesion.
        """
        self._check_login('No se puede ejecutar el metodo: accept_session_cookies()')

        self.wait()
        try:
            #accept_button = self.browser_handler.find_element(By.XPATH, SAVE_SCOOKIES_XPATH)
            accept_button = get_element(self.browser_handler,(By.XPATH, SAVE_SCOOKIES_XPATH))

            #no_accept_button = self.browser_handler.find_element(By.XPATH, DONT_SAVE_SCOOKIES_XPATH)
            no_accept_button = get_element(self.browser_handler,(By.XPATH, DONT_SAVE_SCOOKIES_XPATH))
            if save:
                accept_button.click()
            else:
                no_accept_button.click()
        except Exception:
            warning("No se encuentra la ventana de permanencia.")
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.accept_session_cookies(save)
        finally:
            self.save_cookies('instagram', self.username)
            self.wait('micro')

    def init_cfg(self):
        if self.use_vpn:
            self._init_vpn()

    def register(self, email: str, name: str, username: str, pwd: str, birth: str):
        
        try:
            self._check_login()
            warning('No se puede registrar una nueva cuenta porque hay una sesion activa.')
            return
        except:
            pass

        birth_date = birth.split('/')
        if(len(birth_date) < 3):
            raise RegisterInvalidBirthdate()


        mail_bot = ProtonMail(custom_b_handler = self.browser_handler)
        #mail_bot.init_browser_handler()
        #prev_handle = 
        self.browser_handler.switch_to.new_window('proton')
        mail_bot.init_web()
        mail_bot.register(email, pwd)
        self.browser_handler.switch_to.window(self.whandle)

        warning('Esperando a que el correo madure: 2 min.')
        time.sleep(EMAIL_MADURATION_TIME)

        

        self.browser_handler.get(IG_REGISTRATION_URL)

        
        #Si aparece el popup preguntando si se desea aceptar cookies del sitio le de a aceptar
        try:
            self.wait('micro')
            accept_bt = self.browser_handler.find_element(By.CSS_SELECTOR, 'button[class="_a9-- _ap36 _a9_0"]')
            accept_bt.click()
        except:
            pass

        #self.active_window()

        time.sleep(15)
        try:
            inputs = get_elements(self.browser_handler, (By.TAG_NAME, 'input'))

            inputs[0].send_keys(email+"@proton.me")
            self.wait('small')
            #comprobar validez
            inputs[1].send_keys(name)
            self.wait('small')
            #comprobar validez
            locator = (By.CSS_SELECTOR, f'button[class="{GEN_USER_BT}"]')
            gen_user = get_clickable_element(self.browser_handler, locator)
            gen_user.click()
            #inputs[2].send_keys(username)
            #comprobar validez
            inputs[3].send_keys(pwd)
            self.wait('small')
            #comprobar validez

            inputs[3].send_keys(Keys.ENTER)

            try:
                error_alert = self.browser_handler.find_element(By.CSS_SELECTOR, f'p[id="{REG_ERROR_ALERT_ID}"]')
                if REG_USERNAME_IN_USE in error_alert.text:
                    raise RegisterUsernameInUse(error_alert.text)
                elif REG_INVALID_MAIL in error_alert.text:
                    raise RegisterInvalidEmail(error_alert.text)
                elif REG_INVALID_PWD in error_alert.text:
                    raise RegisterPasswordBelowSix(error_alert.text)
                elif REG_INVALID_USERNAME in error_alert.text:
                    raise RegisterInvalidUsername(error_alert.text)
            except:
                pass


            locator = (By.CSS_SELECTOR, f'select[class="{DATE_SELECTORS}"]')
            selectors = get_elements(self.browser_handler, locator)

            for i in range(3):
                selectors[i].click()

                locator = (By.CSS_SELECTOR, f'option[value="{birth_date[i]}"]')
                cur_opt = get_element(self.browser_handler, locator)

                self.browser_handler.execute_script('arguments[0].scrollIntoView();', cur_opt)
                cur_opt.click()
                self.wait('micro')

            self.wait('micro')

            locator = (By.CSS_SELECTOR, f'button[class="{REG_NEXT_BT}"]')
            next_bt = get_element(self.browser_handler, locator)
            next_bt.click()

            self.wait('micro')

            while True:
                try:
                    self.browser_handler.find_element(By.XPATH, "//*[contains(text(), 'aptcha')]")
                    self.show_window()
                except:
                    break
            
            time.sleep(50)

            

            prev_handle = self.browser_handler.current_window_handle
            self.browser_handler.switch_to.window(mail_bot.whandle)
            ver_code = mail_bot.get_mail_subject('Instagram')
            self.browser_handler.switch_to.window(prev_handle)
            #self.active_window()

            ver_code = ver_code.split()[0]
            print(ver_code)

            locator = (By.CSS_SELECTOR, f'input[class="{VER_CODE_INPUT}"]')
            code_input = get_element(self.browser_handler, locator)
            code_input.click()

            
            locator = (By.CSS_SELECTOR, f'input[class="{VER_CODE_ACTIVE_INPUT}"]')
            code_input = get_element(self.browser_handler, locator)
            code_input.send_keys(ver_code)
            self.wait('micro')
            code_input.send_keys(Keys.ENTER)

            #Aqui deberia llamar algun metodo que revise el correo en busqueda de correo de verificacion y que lo retorne
            

        except Exception as e:
            warning(f'No se puede registrar una nueva cuenta porque no se encontraron algunos elementos\n{e}')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.register(email, name, username, pwd, birth)

    def create_new_account(self) -> tuple[str]:

        self.activate_vpn()
        proton = ProtonMail(use_vpn=True)
        proton.init_browser_handler()
        proton.init_web()
        proton.activate_vpn()
        data = proton.register(gen_email(), gen_pwd())


    def login(self, sv_cookies: bool=False, accept_nt: bool=False):

        if not self.__is_in_page:
            raise PageNotLoaded(IG_URL)
        if self.is_logged:
            warning('login(): No se puede iniciar sesion porque ya se ha iniciado sesion con una cuenta, debe cerrar sesion primero.')
            return

        if not self.username:
            raise LoginNoUserException()
        elif not self.pwd:
            raise LoginNoPasswordException()

        username_input = self.browser_handler.find_element(By.XPATH, USER_INPUT_XPATH)
        pwd_input = self.browser_handler.find_element(By.XPATH, PWD_INPUT_XPATH)
        username_input.send_keys(self.username)
        pwd_input.send_keys(self.pwd)

        try:
            login_button = self.browser_handler.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
            login_button.click()
        except NoSuchElementException:
            raise InvalidInputData()

        self.wait('micro')

        try:
            login_msg = self.browser_handler.find_element(By.XPATH, LOGIN_ERROR_MSG_XPATH)
            if LOGIN_INCORRECT_PWD_MSG in login_msg.text:
                self.is_logged = False
                raise InstagramBadPassword()
        except NoSuchElementException:
            self.is_logged = True
        self.accept_session_cookies(sv_cookies)

        #self.accept_notifications(False)

    def search_for(self, searching:str):
        """
            Busca cuentas o hashtags por medio de la barra de busqueda de la pagina.
        """
        self._check_login("No se pueden buscar cuentas si no se ha iniciado sesion con una cuenta previamente.")

        try:
            search_button = self.browser_handler.find_element(By.CSS_SELECTOR, 'svg[aria-label="Búsqueda"]')
            search_button.click()

        except NoSuchElementException as e:
            warning(f'search_for(): no se encontro el boton de busqueda.:{e}')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.search_for(searching)

        try:
            self.wait()
            search_input = self.browser_handler.find_element(By.CSS_SELECTOR, 'input')
            search_input.send_keys(searching)
            search_input.send_keys(Keys.ENTER)

        except NoSuchElementException as e:
            warning(f'search_for(): no se ha encontrado el input de busqueda.{e}')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.search_for(searching)

        try:
            self.wait()
            element_located = EC.presence_of_element_located
            locator = (By.CSS_SELECTOR, f'a[class="{SEARCH_CANDIDATE_CLASSES}"]')
            result_link = WebDriverWait(self.browser_handler, WAIT_MAX).until(element_located(locator))
            result_link.click()
        except Exception as e:
            warning(repr(e))
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.search_for(searching)


    def logout(self):
        """
        Cierra la sesion actual.
        """
        self._check_login('logout(): No se puede cerrar una sesion si no se ha iniciado sesion antes.')
        self.username = ''
        self.pwd = ''
        #Elimina las cookies de sesion que estan cargadas (si es que las hay)
        self.delete_cookies()
        self.is_logged = False
        self.refresh()


    def close(self):
        try:
            self.logout()
        except NoLoggedSession:
            warning('close(): no hay una sesion abierta')
            pass
        prev_handle = self.browser_handler.current_window_handle
        self.vpn.switch_to_vpn()
        self.vpn.deactivate()
        self.vpn.close()
        self.browser_handler.switch_to.window(prev_handle)
        self.close_browser_handler()

    def open_followers_list(self):
        self._check_login()
        try:
            locator = (By.CSS_SELECTOR, f'ul[class="{AC_INFO_SECTION_CLASSES}"]')

            #Espera hasta que cargue la seccion de informacion de la cuenta (Seguidos, Seguidores, etc)
            #WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            get_element(self.browser_handler, locator)

            followers_link = self.browser_handler.find_element(By.CSS_SELECTOR, f'li[class="{AC_FOLLOWERS_LINK_CLASSES}"]:nth-child(2)')
            followers_link.click()
        except TimeoutError:
            warning('open_followers_list(): no se encontro el link para ver la lista de seguidores')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.open_followers_list()

    def open_following_list(self):
        self._check_login()
        try:
            locator = (By.CSS_SELECTOR, f'ul[class="{AC_INFO_SECTION_CLASSES}"]')

            #Espera hasta que cargue la seccion de informacion de la cuenta (Seguidos, Seguidores, etc)
            #WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            get_element(self.browser_handler, locator)

            followers_link = get_element(self.browser_handler, (By.CSS_SELECTOR, f'li[class="{AC_FOLLOWERS_LINK_CLASSES}"]:nth-child(3)'))
            followers_link.click()
        except TimeoutException:
            warning('open_following_list(): no se encontro el link para ver la lista de seguidos')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.open_following_list()

    def follow_by_hashtag(self, hashtag: str, like_posts: bool, limit: int=30) -> list[str]:
        """
    #       follow_by_Hashtag(hashtag: str, limit: int) -> list[str]

            -Funcion para seguir cuentas aleatorias a partir de los likes
            de un post aleatorio obtenido de un determinado hashtag.

    #       Parametros:

                <hashtag: str> = cadena que representa al hashtag por el cual se elegira una cuenta random
                    para posteriormente revisar y seguir a sus seguidores. Hay menos posibilidades de que instagram
                    detecte al bot si los hashtags que ingresas tienen que ver con la tematica de tu cuenta.

                <limit: int> = limite de cuentas a seguir, se ha puesto como valor default 30 para probar con cuentas nuevas

            -Hay que tener cuidado a la hora de especificar el max_follow, ya que
            instagram tiene un limite de 60 seguidas por hora y 150 por dia.
            Ademas es mas limitado cuando la cuenta es nueva.

    #        Valor de retorno: list[str]

                -retorna la lista de cuentas seguidas.
        """
        #if not self.is_logged:
        #    raise NoLoggedSession('No se puede buscar cuentas por hashtag si no se ha iniciado sesion con una cuenta previamente.')

        self.search_for(hashtag)
        self.wait('micro')

        #self.browser_handler.get(IG_EXPLORE_TAG+hashtag)
        #Verifica si hay resultados para el hashtag ingresado
        try:
            #self.browser_handler.find_element(By.XPATH, "//span[contains(text(),'{}')]".format(NOT_FOUND_MSG))
            get_element(self.browser_handler, (By.XPATH, f"//span[contains(text(),'{NOT_FOUND_MSG}')]"))
            raise ResultsNotFound(hashtag)
        except NoSuchElementException:
            pass

        #self.wait()

        print('->'+ self.browser_handler.current_url)

        account_list = []
        account_users = []

        try:

            rows_locator = (By.CSS_SELECTOR, 'div[class="_ac7v  _al3n"]')
            #rows = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_all_elements_located(rows_locator))
            rows = get_elements(self.browser_handler, rows_locator)
            i = secrets.randbelow(len(rows)-1)

            #cols_locator = (By.CSS_SELECTOR, 'div[class="_aabd _aa8k  _al3l"]')
            #cols = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_all_elements_located(cols_locator))
            cols = rows[i].find_elements(By.CSS_SELECTOR, 'div[class="_aabd _aa8k  _al3l"]')
            j = secrets.randbelow(len(cols)-1)

            post_link = cols[j].find_element(By.TAG_NAME, 'a')
            post_link.click()
        except Exception as e:
            warning(f'follow_by_hashtag(): no se encuentran las filas de la matriz de posts.: {e}')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                account_users = self.follow_by_hashtag(hashtag, like_posts, limit)


        try:
            self.wait('nano')
            #initial_account = self.browser_handler.find_element(By.CSS_SELECTOR, f'a[class="{POST_ACCOUNT_LINK_CLASSES}"]')
            initial_account = get_element(self.browser_handler, (By.CSS_SELECTOR, f'a[class="{POST_ACCOUNT_LINK_CLASSES}"]'))
            initial_account.click()

        except NoSuchElementException as e:
            warning(f"follow_by_hashtag(): no se encuentra el link de la cuenta propietaria del post.:{e}")
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                account_users = self.follow_by_hashtag(hashtag, like_posts, limit)

        try:
            self.wait('micro')
            self.open_followers_list()
            self.wait()

            #Reduce el tamaño de la ventana para que aparezca la scroll bar y asi poder actualizar la lista de seguidores
            #   ya que por algun motivo que desconozco al bajar la scroll bar del widget de la lista de seguidores hasta el final
            #   esta lista no se actualiza y solo se actualiza cuando estoy en el final y subo y bajo el scroll bar de la ventana de la pagina.
            self.browser_handler.set_window_size(412, 400)
            locator = (By.CSS_SELECTOR, f'div[class="{AC_FOLLOWERS_SEC_CLASS}"]')
            followers_box = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))

            locator = (By.CSS_SELECTOR, f'div[class="{AC_FOLLOWER_CLASSES}"]')

            #bucle que actualiza la lista de seguidores hasta que la cantidad coincida con el limite especificado previamente
            attempt = 0
            prev_len = 0
            while True:

                self._update_follow_list(followers_box)
                #followers_list = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_all_elements_located(locator))
                followers_list = get_elements(self.browser_handler, locator)
                followers_len = len(followers_list)

                if (followers_len >= limit) or (attempt > 4):
                    account_list = followers_list
                    break
                elif followers_len == prev_len:
                    attempt+=1
                else:
                    prev_len = followers_len


            for account in account_list:
                ac_span = account.find_element(By.CSS_SELECTOR, f'span[class="{AC_FOLLOWER_NAME_CLASSES}"]')
                ac_follow_bt = account.find_element(By.CSS_SELECTOR, f'button[class="{AC_FOLLOWER_FOLLOW_BT_CLASSES}"]')

                self.browser_handler.execute_script('arguments[0].scrollIntoView()', ac_follow_bt)
                account_users.append(ac_span.text)

                following = ('Siguiendo' in ac_follow_bt.text) or ('Soli' in ac_follow_bt.text)
                if not following:
                    ac_follow_bt.click()
                self.wait('micro')

        except NoSuchElementException as e:
            warning(f"follow_by_hashtag(): no se encuentra el link para ver seguidores de la cuenta.:{e}")
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                account_users = self.follow_by_hashtag(hashtag, like_posts, limit)

        return account_users

    def like_posts(self, user: str, limit: int = 3):
        """
            metodo que da like a una cantidad de posts especificada por limit de una cuenta especificada por user
        """
        prev_url = self.browser_handler.current_url
        self.browser_handler.get(f"https://www.instagram.com/{user}")
        try:
            post_rows = get_elements(self.browser_handler, (By.CSS_SELECTOR, f'div[class="{POST_ROW}"]'))
            counter = 0

            for row in post_rows:
                post_links = row.find_elements(By.TAG_NAME, 'a')
                for link in post_links:
                    if(counter >= limit):
                        break
                    link.click()

                    like_bt = get_element(self.browser_handler, (By.CSS_SELECTOR, 'svg[aria-label="Me gusta"]'))
                    like_bt.click()

                    self.wait('nano')
                    close_bt = get_element(self.browser_handler, (By.CSS_SELECTOR, 'svg[aria-label="Cerrar"]'))
                    close_bt.click()
                    counter+=1
            self.browser_handler.get(prev_url)
        except Exception as e:
            warning(f'No se pudo darle like a un post de la cuenta: {user}')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.like_posts(user, limit)

        #---------- En desarrollo ----------


    def _update_follow_list(self, follow_box):
        self.browser_handler.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", follow_box)
        self.wait('nano')
        self.browser_handler.execute_script("window.scrollTo(0,0)")
        self.wait('nano')
        self.browser_handler.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        self.wait('micro')

    def open_my_profile(self):
        """
            abre la pagina del perfil de la cuenta que esta usando el bot
        """
        self._check_login()
        #print('->'+ self.browser_handler.current_url)

        self.wait('nano')
        try:
            locator = (By.CSS_SELECTOR, f'div[class="{LEFT_BAR_DIV_CLASS}"]')
            left_bar = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            my_profile_link = left_bar.find_element(By.CSS_SELECTOR, 'div:nth-child(8)')
            my_profile_link.click()
        except TimeoutException:
            warning('No se encontro el link para ver el perfil de la cuenta.')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.open_my_profile()

        #print('->'+ self.browser_handler.current_url)


    def my_followers_num(self) -> int:
        """
            retorna el numero de seguidores actual de la cuenta que usa el bot
        """
        #self._check_login()
        self.open_my_profile()
        print('->'+ self.browser_handler.current_url)
        followers_num = None
        try:

            locator = (By.CSS_SELECTOR, f'ul[class="{AC_INFO_SECTION_CLASSES}"]')

            #Espera hasta que cargue la seccion de informacion de la cuenta (Seguidos, Seguidores, etc)
            WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))

            followers_link = self.browser_handler.find_element(By.CSS_SELECTOR, f'li[class="{AC_FOLLOWERS_LINK_CLASSES}"]:nth-child(2)')
            followers_num = int(followers_link.text.replace(' seguidores', ''))

            #followers_num = int(num_span.text)

        except TimeoutException:
            warning('No se encontro el numero de seguidores de la cuenta.')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                followers_num = self.my_followers_num()

        return followers_num

    def unfollow_users(self, users: list[str]):
        """
        Esta funcion deja de seguir una lista de usuarios (users: list[str])
        """
        self.open_my_profile()
        self.open_following_list()

        for user in users:
            try:
                search_user_input = get_element(self.browser_handler, (By.CSS_SELECTOR, 'input[aria-label="Buscar entrada"]'))
                search_user_input.send_keys(user)
                search_user_input.send_keys(Keys.ENTER)

                self.wait('search')
                unfollow_bt = get_element(self.browser_handler, (By.CSS_SELECTOR, f'button[class="{UNFOLLOW_BT}"]'))
                unfollow_bt.click()
                accept_bt = get_element(self.browser_handler, (By.CSS_SELECTOR, f'button[class="{ACCEPT_UNFOLLOW}"]'))
                accept_bt.click()
            except Exception as e:
                warning(f'no se encontro a {user}')
                if self.check_challenge():
                    while 'challenge' in self.browser_handler.current_url:
                        warning('Se debe resolver el captcha para poder continuar.')
                        self.wait()
                    self.unfollow_users(users)



    def upload_post(self, post_img_path: str, post_txt: str=''):
        """
            Esta funcion sube una publicacion a la cuenta, post_img_path es la cadena donde va la ruta de la imagen a postear
            y post_txt la cadena donde va la descripcion del post.
        """
        self.wait('micro')
        try:
            locator = (By.CSS_SELECTOR, 'svg[aria-label="Nueva publicación"]')
            #upload_post_bt = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            upload_post_bt = get_element(self.browser_handler, locator)
            upload_post_bt.click()

            locator = (By.CSS_SELECTOR, f'input[class="{SECRET_IGM_INPUT_CLASS}"]')
            img_input = get_element(self.browser_handler, locator)
            img_input.send_keys(post_img_path)
            self.wait('nano')

            locator = (By.CSS_SELECTOR, f'div[class="{POST_NEXT_BT}"]')
            next_bt = get_element(self.browser_handler, locator)
            next_bt.click()
            self.wait('nano')
            next_bt = get_element(self.browser_handler, locator)
            next_bt.click()

            if post_txt:
                locator = (By.CSS_SELECTOR, f'div[class="{POST_DESC_INPUT_CLASS}"]')
                desc_input = get_element(self.browser_handler, locator)
                desc_input.send_keys(post_txt)

            locator = (By.CSS_SELECTOR, f'div[class="{POST_NEXT_BT}"]')
            upload_bt = get_element(self.browser_handler, locator)
            upload_bt.click()

            try:
                get_element(self.browser_handler, (By.CSS_SELECTOR, f'span[class="{POST_UPLOAD_SUCCESS}"]'))
                print('Post subido exitosamente!.')
            except TimeoutException:
                warning('Tiempo de espera para subir el post excedido')
                self.check_challenge()

            locator = (By.CSS_SELECTOR, 'svg[aria-label="Cerrar"]')
            close_bt = get_element(self.browser_handler, locator)
            close_bt.click()

            #if post_place:
            #    locator = (By.CSS_SELECTOR, f'div[class="{PLACE_INPUT_CLASS}"]')
            #    place_input = get_element(self.browser_handler, locator)
            #    place_input.send_keys(post_place)
        except TimeoutException:
            warning('No se ha encontrado el boton para subir posts.')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.upload_post(post_img_path, post_txt)

    def comment_post(self, post_url: str, comment_txt: str):
        """
            Metodo que hace comentario en un post dado por su url
        """

        #prev_url = self.browser_handler.current_url
        self.browser_handler.get(post_url)
        self.wait('nano')
        try:
            #Presiona el cuadro de texto para activarlo
            locator = (By.CSS_SELECTOR, f'textarea[class="{OFF_COMMENT_TEXT}"]')
            comment_input = get_element(self.browser_handler, locator)
            comment_input.click()

            #Una vez activado se escribe el comentario
            locator = (By.CSS_SELECTOR, f'textarea[class="{ON_COMMENT_TEXT}"]')
            comment_input = get_element(self.browser_handler, locator)
            comment_input.send_keys(comment_txt)

            #Y luego se presiona el boton de publicar
            locator = (By.CSS_SELECTOR, f"div[class={SEND_COMMENT_BT}]")
            comment_bt = get_element(self.browser_handler, locator)
            comment_bt.click()
        except StaleElementReferenceException:
            warning('No se activo el cuadro de texto y por lo tanto no se puede escribir el comentario')
        except TimeoutException:
            warning(f'No se pudo comentar en el post: {post_url}')
            if self.check_challenge():
                while 'challenge' in self.browser_handler.current_url:
                    warning('Se debe resolver el captcha para poder continuar.')
                    self.wait()
                self.comment_post(post_url, comment_txt)

        #self.browser_handler.get(prev_url)

    def comment_post_list(self, post_url_list: list[str], comment_txt: str):
        """
            Metodo que hace un comentario a una lista de posts dados por su url
        """
        for post_url in post_url_list:
            self.comment_post(post_url, comment_txt)

    def check_challenge(self) -> bool:
        """
            Metodo que verifica si instagram esta solicitando resolver un "desafio" o captcha para comprobar que no eres un bot

            Se recomienda que despues de una sospecha por parte de ig la cantidad de cuentas a seguir o dejar de seguir y la cantidad de likes
            disminuya a la mitad o mas, de otro modo se corre el riesgo de otras penalizaciones como ban.
        """
        if 'challenge' in self.browser_handler.current_url:
            warning("Posible deteccion del bot: Se requiere verificacion por recaptcha")
            self.show_window()
            return True

        return False

    def _check_login(self, admsg:str=''):
        if not self.is_logged:
            raise NoLoggedSession(admsg)
#<------------------------------><------------------------------><------------------------------>


def main():
    #vpn = UrbanVpn()
    #vpn.init_browser_handler()
    #vpn.init_page()
        
    #proton = ProtonMail(use_vpn=True)

    #proton.init_browser_handler()
    #proton.init_web()
    #proton.activate_vpn()
    #proton.register("ayahuasca3240", "987659821.")
    #print(proton.create_new_account())
    bot = IgBot(use_vpn=True)
    #bot.set_username('darkm31')
    #bot.pwd = 'password'

    bot.init_browser_handler()
    #bot.init_ig()

    #bot.create_new_account()
    #bot.close()
    #bot.init_cfg()
    bot.init_ig()
    bot.register(gen_email(), gen_name(), 'wasridss2', gen_pwd(), gen_birth())
    #bot.wait('micro')
    #bot.show_window()
    #bot.accept_notifications(False)
    #bot.comment_post('https://www.instagram.com/p/C3tRu41pVEE/', '.')
    #bot.unfollow_users(['lucasmeloryt'])
    #bot.like_posts('lucasmeloryt')
    #bot.upload_post('Desktop/kk.png', 'Somethingsomethingsomething')
    #print(bot.my_followers_num())
    #print(bot.follow_by_hashtag('#programacionvenezuela'))
    #time.sleep(1000)

    #bot.close()

if __name__ == "__main__":
    main()
