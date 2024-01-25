""" 
    Bot para Instagram 
    Autor: Miguel Matute
    Fecha: 05/01/2024

    Descripcion:
        -este bot usa la api de selenium para las interacciones con los diferentes elementos de las paginas y para web scrapping
    Notas del autor:
        -durante todas las pruebas, instagram no ha detectado actividad sospechosa. Pero esto no quiere decir que no pueda detectarla.
        -El uso prolongado del bot puede levantar sospechas por parte de instagram, cosa que no me ha pasado hasta ahora por suerte.
"""

import time
#import random
import os
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

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from win32gui import GetWindowText
from win32gui import EnumWindows
from win32gui import ShowWindow

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
        webdriver_path+= "chromedriver.exe"
    elif "Firefox" in browser_type:
        webdriver_path+= "geckodriver.exe"
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

get_element = lambda bhandler, locator: WebDriverWait(bhandler, WAIT_MAX).until(EC.presence_of_element_located(locator))
"""
    funcion que espera 60 segundos a que un elemento cargue y luego lo retorna
"""
get_elements = lambda bhandler, locator: WebDriverWait(bhandler, WAIT_MAX).until(EC.presence_of_all_elements_located(locator))
"""
    funcion que espera 60 segundos a que todos los elementos especificador por el locator esten cargados luego devuelve la lista de los elementos 
"""

#<------------------------------><------------------------------><------------------------------>
class Browser:
    """
        Clase Browser:

        -- propiedades:
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
    def __init__(self, browser_path: str='', use_vpn: bool = False, headless: bool = False):
        self.webdriver_path = None
        self.def_browser = None
        self.is_headless = headless
        self.use_vpn = use_vpn
        self.__is_hide = False

        if(not browser_path):
             self.def_browser = default_browser.get_browser_exepath()
        else:
            self.def_browser = browser_path
        self.webdriver_path = get_webdriver_path(self.def_browser)

        self.browser_handler = None
        self.options = None
        self.service = None
        self.sleep_secs = None

    def _init_chrome(self):
        self.options = COptions()
        #full_userdata_path = os.path.join(os.getcwd(), CHROME_USER_DATA)
        #self.options.add_argument(f"--user-data-dir={CHROME_USER_DATA}")
        #if self.is_headless:
            #ejecuta el programa sin la ventana del navegador
        #    self.options.add_argument('--headless=new')
        #    self.options.add_experimental_option('prefs', {'intl.accept_languages': 'es,es_ES'})
        if self.use_vpn:
            full_path = os.path.join(os.getcwd(), URBAN_VPN_EXT_PATH)
            self.options.add_argument(f'--load-extension={full_path}')
        #full_profile_path = os.path.join(os.getcwd(), PROFILE_PATH)
        self.options.add_argument(f'--profile-directory=Default')

        #Este parametro evita que aparezca el mensaje "Un software automatizado esta controlando chrome"
        self.options.add_experimental_option('excludeSwitches', ["enable-automation"])

        #Este parametro permite que la ventana del navegador permanezca abierta aun despues de haber realizado alguna tarea.
        self.options.add_experimental_option('detach', True)

        self.options.binary_location = self.def_browser
        self.service = CService(executable_path=self.webdriver_path)
        self.browser_handler = webdriver.Chrome(options=self.options, service=self.service)

    def _init_firefox(self):
        self.options = FOptions()
        self.options.binary = self.def_browser
        self.service = FService(executable_path=self.webdriver_path)
        self.browser_handler = webdriver.Firefox(options=self.options, service=self.service)

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

    def init_browser_handler(self):
        """"
            Inicializa el webdriver
        """
        if "Chrome" in self.def_browser:
            self._init_chrome()

        #!!IMPORTANTE!!: Firefox perdera soporte por falta de metodos para evadir la deteccion de bots.
        elif "Firefox" in self.def_browser:
            self._init_firefox()
        else:
            raise UncompatibleDefaultBrowser(self.def_browser)
        

    def save_cookies(self, webname: str, username: str):

        #Por el momento almaceno las cookies en archivos JSON
        #Mas tarde implementare el guardado de cookies en una base de datos sqlite
        cookies = self.browser_handler.get_cookies()

        #with open(COOKIES_PATH+pre+'_cookies.json', 'w+') as file_cookie:
        #    json.dump(cookies, file_cookie)

        data.db_save_cookies(COOKIES_DB, webname, username, cookies)

    def delete_cookies(self):
        self.browser_handler.delete_all_cookies()

    def load_cookies(self, webname: str, username: str):
        """
            Carga las cookies de sesion de una red social determinada
            por el parametro 'pre', el cual es una cadena que contiene
            el prefijo de la red social. Ejem: ig (Instagram), fb (Facebook),
            ttk (TikTok), etc...
        """
        try:
            #with open(COOKIES_PATH+pre+'_cookies.json', 'r') as file_cookie:
            #    cookies = json.load(file_cookie)

            cookies = data.db_load_cookies(COOKIES_DB, webname, username)
            
            self.browser_handler.execute_cdp_cmd('Network.enable',{})

            for cookie in cookies:
                #cookie['domain'] = cookie['domain'].replace(self.old_url, self.url)
                self.browser_handler.execute_cdp_cmd('Network.setCookie', cookie)
            #    self.browser_handler.add_cookie(cookie)
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
            type: parametro que representa la forma en la que se refrescan los segundos de espera (tiempo de espera normal, pequeño, micro o nano)
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
class UrbanVpn:
    
    def __init__(self,
                 h_browser: webdriver.Chrome,
                 #country: str,
                 #ad_block: bool,
                 #anti_phish: bool
                 ):
        self.browser_handler = h_browser
        #self.country = country
        #self.ad_block = ad_block
        #self.anti_phish = anti_phish
        self.__is_in_page = False

        
    def init_page(self):
        self.browser_handler.implicitly_wait(4)
        self.browser_handler.get(URBAN_VPN_LINK)
        self.__is_in_page = True
        
        WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.number_of_windows_to_be(2))
        current_handle = self.browser_handler.current_window_handle
        
        for handle in self.browser_handler.window_handles:
            if handle != current_handle:
                self.browser_handler.switch_to.window(handle)
                self.browser_handler.close()
                break
        self.browser_handler.switch_to.window(current_handle)
        self.accept_terms()
        
    
    def accept_terms(self):
        #WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located((By.CLASS_NAME, 'promotion__text')))
        get_element(self.browser_handler, (By.CLASS_NAME, 'promotion__text'))

        try:
            #terms_button = self.browser_handler.find_element(By.CLASS_NAME, 'consent-text-controls__action')
            terms_button = get_element(self.browser_handler, (By.CLASS_NAME, 'consent-text-controls__action'))
            terms_button.click()
            self.browser_handler.implicitly_wait(1)
            
            #self.browser.save_cookies('vpn')
        except NoSuchElementException:
            #warning('no cargo la pagina para aceptar terminos')
            pass
        

    def activate(self):
        
        if not self.__is_in_page:
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

            index = secrets.randbelow(len(countries_list))
            self.browser_handler.execute_script("arguments[0].scrollIntoView();", countries_list[index])
            countries_list[index].click()

            #run_button = self.browser_handler.find_element(By.CLASS_NAME, 'play-button--play')
            #run_button.click()

            #WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located((By.CLASS_NAME, 'play-button--pause')))
            get_element(self.browser_handler, (By.CLASS_NAME, 'play-button--pause'))
            #print('listo')
        except TimeoutException as e:
            warning('No se encontraron elementos necesarios para activar el vpn')
            warning(repr(e))

    def deactivate(self):
        #stop_button = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located((By.CLASS_NAME, 'play-button--pause')))
        stop_button = get_element(self.browser_handler, (By.CLASS_NAME, 'play-button--pause'))
        stop_button.click()

    def close(self):
        self.__is_in_page = False
        #self.browser_handler.close()
    

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
                
                * init_ig_main():
                    carga la pagina principal de instagram
                
                * login(user: str, pwd: str):
                    inicia sesion con una cuenta en instagram 
    """
    def __init__(self,
                 username: str='',
                 pwd: str='',
                 browser_path: str ='',
                 use_vpn: bool = False,
                 headless:bool = False):
        
        self.username = username
        self.pwd = pwd
        self.vpn = None
        self.is_logged = False
        self.__is_in_page = False

        super().__init__(browser_path, use_vpn, headless)
        self.init_browser_handler()


    #Solo ignoren este metodo XD
    #def _exist_usercookie(self, username: str) -> bool:
    #    flg = False
    #    for arch in os.listdir(COOKIES_PATH):
    #        if username in arch:
    #            flg = True
    #            break
    #    return flg
        
    def _init_vpn(self):
        self.vpn = UrbanVpn(self.browser_handler)
        self.vpn.init_page()

        

        self.vpn.accept_terms()
        self.vpn.activate()
        self.wait('micro')

    def init_ig(self, preload_cookies:bool = True):
        """
            Metodo que inicializa el vpn, carga las cookies de sesion e inicia la pagina principal de instagram
        """

        if self.is_headless:
            self.hide_window(inital_page=True)
        if self.use_vpn:
            self._init_vpn()
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
                raise IgUsernameNotFound()
        
        self.browser_handler.get(IG_URL)
        self.__is_in_page = True

        if not self.is_logged:
            self.login(True, False)

    def accept_notifications(self, accept: bool):
        """
            da click en aceptar o rechazar en la ventana emergente de notificaciones dependiendo del parametro accept
        """
        self._check_login('No se puede ejecutar el metodo: accept_notifications()')
        
        self.wait('micro')
        try:
            locator = (By.CSS_SELECTOR, f'button[class="{ACCEPT_NOTIFICATIONS_SL}"]')
            #accept_button = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            accept_button = get_element(self.browser_handler, locator)

            locator = (By.CSS_SELECTOR, f'button[class="{DONT_ACCEPT_NOTIFICATIONS_SL}"]')
            #no_accept_button = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            no_accept_button = get_element(self.browser_handler, locator)
            #accept_button = self.browser_handler.find_element(By.CSS_SELECTOR, ACCEPT_NOTIFICATIONS_SL)
            #no_accept_button = self.browser_handler.find_element(By.CSS_SELECTOR, DONT_ACCEPT_NOTIFICATIONS_SL)

            if accept:
                accept_button.click()
            else:
                no_accept_button.click()
        except Exception:
            warning("No se encuentra la ventana de notificaciones.")

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
        finally:
            self.save_cookies('instagram', self.username)
            self.wait()
        

    def login(self, sv_cookies: bool=False, accept_nt: bool=False):
        
        if not self.__is_in_page:
            raise PageNotLoaded(IG_URL)
        if self.is_logged:
            warning('login(): No se puede iniciar sesion porque ya se ha iniciado sesion con una cuenta, debe cerrar sesion primero.')
            return
        
        if not self.username:
            raise LoginNoUserException
        elif not self.pwd:
            raise LoginNoPasswordException

        username_input = self.browser_handler.find_element(By.XPATH, USER_INPUT_XPATH)
        pwd_input = self.browser_handler.find_element(By.XPATH, PWD_INPUT_XPATH)
        username_input.send_keys(self.username)
        pwd_input.send_keys(self.pwd)

        try:
            login_button = self.browser_handler.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
            login_button.click()
        except NoSuchElementException:
            raise InvalidInputData()
            
        self.wait()

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
        
        try:
            self.wait()
            search_input = self.browser_handler.find_element(By.CSS_SELECTOR, 'input')
            search_input.send_keys(searching)
            search_input.send_keys(Keys.ENTER)
            
        except NoSuchElementException as e:
            warning(f'search_for(): no se ha encontrado el input de busqueda.{e}')
        
        try:
            self.wait()
            element_located = EC.presence_of_element_located
            locator = (By.CSS_SELECTOR, f'a[class="{SEARCH_CANDIDATE_CLASSES}"]')
            result_link = WebDriverWait(self.browser_handler, WAIT_MAX).until(element_located(locator))
            result_link.click()
        except Exception as e:
            warning(repr(e))
        
        
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


    def close(self):
        try:
            self.logout()
        except NoLoggedSession:
            warning('close(): no hay una sesion abierta')
            pass
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
    
    def follow_by_hashtag(self, hashtag: str, limit: int=30) -> list[str]:
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
        self.wait('small')

        #self.browser_handler.get(IG_EXPLORE_TAG+hashtag)
        #Verifica si hay resultados para el hashtag ingresado
        try:
            self.browser_handler.find_element(By.XPATH, "//span[contains(text(),'{}')]".format(NOT_FOUND_MSG))
            raise ResultsNotFound(hashtag)
        except NoSuchElementException:
            pass
        
        #self.wait()

        print('->'+ self.browser_handler.current_url)

        account_list = []

        try:
            
            rows_locator = (By.CSS_SELECTOR, 'div[class="_ac7v  _al3n"]')
            rows = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_all_elements_located(rows_locator))
            i = secrets.randbelow(len(rows)-1)

            cols_locator = (By.CSS_SELECTOR, 'div[class="_aabd _aa8k  _al3l"]')
            cols = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_all_elements_located(cols_locator))
            j = secrets.randbelow(len(cols)-1)

            post_link = cols[j].find_element(By.TAG_NAME, 'a')
            post_link.click()
        except NoSuchElementException as e:
            warning(f'follow_by_hashtag(): no se encuentran las filas de la matriz de posts.: {e}')


        try:
            self.wait('micro')
            initial_account = self.browser_handler.find_element(By.CSS_SELECTOR, f'a[class="{POST_ACCOUNT_LINK_CLASSES}"]')
            initial_account.click()

        except NoSuchElementException as e:
            warning(f"follow_by_hashtag(): no se encuentra el link de la cuenta propietaria del post.:{e}")
        
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
            while True:
                self.browser_handler.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", followers_box)
                self.wait('nano')
                self.browser_handler.execute_script("window.scrollTo(0,0)")
                self.wait('nano')
                self.browser_handler.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                self.wait('micro')
                followers_list = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_all_elements_located(locator))
                if len(followers_list) >= limit:
                    account_list = followers_list
                    break

            account_users = []
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

        return account_users
    
    def open_my_profile(self):
        """
            abre la pagina del perfil de la cuenta que esta usando el bot
        """
        self._check_login()
        print('->'+ self.browser_handler.current_url)
        
        self.wait('nano')
        try:
            locator = (By.CSS_SELECTOR, f'div[class="{LEFT_BAR_DIV_CLASS}"]')
            left_bar = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            my_profile_link = left_bar.find_element(By.CSS_SELECTOR, 'div:nth-child(8)')
            my_profile_link.click()
        except TimeoutException:
            warning('No se encontro el link para ver el perfil de la cuenta.')
            
        print('->'+ self.browser_handler.current_url)


    def my_followers_num(self) -> int:
        """
            retorna el numero de seguidores actual de la cuenta que usa el bot
        """
        #self._check_login()
        self.open_my_profile()
        print('->'+ self.browser_handler.current_url)
        followers_num = None
        try:
            #locator = (By.CSS_SELECTOR, f'span[class="{NUM_SPAN_CLASSES}"]:nth-child(2)')
            #locator = (By.PARTIAL_LINK_TEXT, ' seguidores')
            #followers_link = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            #num_span = followers_link.find_element(By.CSS_SELECTOR, 'span > span')
            #num_span = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))

            locator = (By.CSS_SELECTOR, f'ul[class="{AC_INFO_SECTION_CLASSES}"]')

            #Espera hasta que cargue la seccion de informacion de la cuenta (Seguidos, Seguidores, etc)
            WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
                
            followers_link = self.browser_handler.find_element(By.CSS_SELECTOR, f'li[class="{AC_FOLLOWERS_LINK_CLASSES}"]:nth-child(2)')
            followers_num = int(followers_link.text.replace(' seguidores', ''))

            #followers_num = int(num_span.text)

        except TimeoutException:
            warning('No se encontro el numero de seguidores de la cuenta.')
        
        return followers_num

    #def is_following_me(self, user:str) -> bool:
    #    pass

    #def are_following_me(self, users: list[str]) -> bool:
    #    pass

    def unfollow_users(self, users: list[str]):
        self.open_my_profile()
        self.open_following_list()


        

    def upload_post(self, post_img_path: str, post_txt: str=''):
        
        self.wait('micro')
        try:
            locator = (By.CSS_SELECTOR, 'svg[aria-label="Nueva publicación"]')
            #upload_post_bt = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            upload_post_bt = get_element(self.browser_handler, locator)
            upload_post_bt.click()

            #locator = (By.CSS_SELECTOR, f'button[class="{SELECT_IMG_BT}"]')
            ##select_img_bt = WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            #select_img_bt = get_element(self.browser_handler, locator)
            #select_img_bt.click()
            
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
            
            locator = (By.CSS_SELECTOR, 'svg[aria-label="Cerrar"]')
            close_bt = get_element(self.browser_handler, locator)
            close_bt.click()

            #if post_place:
            #    locator = (By.CSS_SELECTOR, f'div[class="{PLACE_INPUT_CLASS}"]')
            #    place_input = get_element(self.browser_handler, locator)
            #    place_input.send_keys(post_place)
        except TimeoutException:
            self.check_challenge()
            warning('No se ha encontrado el boton para subir posts.')

    def check_challenge(self):
        if 'challenge' in self.browser_handler.current_url:
            self.show_window()

    def _check_login(self, admsg:str=''):
        if not self.is_logged:
            raise NoLoggedSession(admsg)
#<------------------------------><------------------------------><------------------------------>
    

def main():
    bot = IgBot()
    bot.username = 'darkm31'
    
    bot.init_ig()
    bot.accept_notifications(False)
    bot.upload_post('C:/Users/Ines/Desktop/kk.png', 'Somethingsomethingsomething')
    #print(bot.my_followers_num())
    #print(bot.follow_by_hashtag('#programacionvenezuela'))
    #time.sleep(1000)

    #bot.close()

if __name__ == "__main__":
    main()
