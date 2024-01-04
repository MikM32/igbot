""" Bot de Instagram """
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.firefox.service import Service as FService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import default_browser
import time
#import random
import json
import os
import secrets

from bot_exceptions import *
from constants import *

def get_webdriver_path(browser_type: str) -> str:
    webdriver_path= WEBDRIVER_ROOT_PATH

    if "Chrome" in browser_type:
        webdriver_path+= "chromedriver.exe"
    elif "Firefox" in browser_type:
        webdriver_path+= "geckodriver.exe"
    else:
        raise UncompatibleDefaultBrowser(browser_type)
    
    return webdriver_path

class Browser:
    """
        Clase Browser:

        -- propiedades:
            -browser_handler: handler del navegador

            -def_browser: cadena que contiene el directorio donde se encuentra el ejecutable del navegador predeterminado

            -options: objeto que contiene los parametros con los cual arrancara el navegador

            -service: objeto que contiene la informacion del webdriver que sera utilizado por el browser_handler

            -sleep_secs: entero que contiene la cantidad de segundos que usara la funcion Browser.wait()

        -- Metodos:
            -
    """
    def __init__(self, browser_path: str='', use_vpn: bool = False, headless: bool = False):
        self.webdriver_path = None
        self.def_browser = None
        self.is_headless = headless
        self.use_vpn = use_vpn

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
        if self.is_headless:
            #ejecuta el programa sin la ventana del navegador
            self.options.add_argument('--headless')
        if self.use_vpn:
            full_path = os.path.join(os.getcwd(), URBAN_VPN_EXT_PATH)
            self.options.add_argument(f'--load-extension={full_path}')
        #full_profile_path = os.path.join(os.getcwd(), PROFILE_PATH)
        self.options.add_argument(f'--profile-directory=Default')

        #Este parametro evita que aparezca el mensaje "Un software automatizado esta controlando chrome"
        self.options.add_experimental_option('excludeSwitches', ["enable-automation"])

        self.options.binary_location = self.def_browser
        self.service = CService(executable_path=self.webdriver_path)
        self.browser_handler = webdriver.Chrome(options=self.options, service=self.service)

    def _init_firefox(self):
        self.options = FOptions()
        self.options.binary = self.def_browser
        self.service = FService(executable_path=self.webdriver_path)
        self.browser_handler = webdriver.Firefox(options=self.options, service=self.service)

    def init_browser_handler(self):
        if "Chrome" in self.def_browser:
            self._init_chrome()
        elif "Firefox" in self.def_browser:
            self._init_firefox()
        else:
            raise UncompatibleDefaultBrowser(self.def_browser)
        

    def save_cookies(self, pre: str):

        #Por el momento almaceno las cookies en archivos JSON
        #Mas tarde implementare el guardado de cookies en una base de datos sqlite
        cookies = self.browser_handler.get_cookies()

        with open(COOKIES_PATH+pre+'_cookies.json', 'w+') as file_cookie:
            json.dump(cookies, file_cookie)

    def delete_cookies(self):
        self.browser_handler.delete_all_cookies()

    def load_cookies(self, pre: str):
        """
            Carga las cookies de sesion de una red social determinada
            por el parametro 'pre', el cual es una cadena que contiene
            el prefijo de la red social. Ejem: ig (Instagram), fb (Facebook),
            ttk (TikTok), etc...
        """
        try:
            with open(COOKIES_PATH+pre+'_cookies.json', 'r') as file_cookie:
                cookies = json.load(file_cookie)
            
            self.browser_handler.execute_cdp_cmd('Network.enable',{})

            for cookie in cookies:
                #cookie['domain'] = cookie['domain'].replace(self.old_url, self.url)
                self.browser_handler.execute_cdp_cmd('Network.setCookie', cookie)
            #    self.browser_handler.add_cookie(cookie)
            self.refresh()

            self.browser_handler.execute_cdp_cmd('Network.disable', {})
        except FileNotFoundError:
            raise CookiesDontExists(pre)     

    def refresh(self):
        if not self.browser_handler:
            raise NotInitizalizedHandler()
        self.browser_handler.refresh()      
        
    def wait(self, type: str=''):
        """
            Metodo que hace esperar al navegador unos segundos
            (Dificulta la deteccion del bot)
            type: parametro que representa la forma en la que se refrescan los segundos de espera (tiempo de espera normal, pequeño o micro)
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
        else:
            #Raise Excepcion
            return

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

class IgBot(Browser):
    """
        Clase IgBot:

            --Propiedades:

                -username: nombre de usuario de la cuenta con la que se esta trabajando

                -is_logged: booleano que determina si la sesion ya esta iniciada

            --Metodos:

                -__init__(*args):
                    args contiene un parametro opcional que seria la ruta del webdriver especificada por el usuario

                -init_ig_main():
                    carga la pagina principal de instagram

                -login(user: str, pwd: str):
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

    def init_ig(self, preload_cookies:bool = True):
        self.browser_handler.implicitly_wait(5)
        if preload_cookies:
            if self.username:
                try:
                    self.load_cookies(f'ig_{self.username}')
                    self.is_logged = True
                except CookiesDontExists as e:
                    warning(f'Error al cargar cookies de sesion para {self.username}: {e}')
                    self.is_logged = False
            else:
                raise IgUsernameNotFound()
            
        self.browser_handler.get(IG_URL)
        self.__is_in_page = True

    def accept_notifications(self, accept: bool):
        if not self.is_logged:
            raise NoLoggedSession('No se puede ejecutar el metodo: accept_notifications()')
        
        self.wait()
        try:
            accept_button = self.browser_handler.find_element(By.CSS_SELECTOR, ACCEPT_NOTIFICATIONS_SL)
            no_accept_button = self.browser_handler.find_element(By.CSS_SELECTOR, DONT_ACCEPT_NOTIFICATIONS_SL)

            if accept:
                accept_button.click()
            else:
                no_accept_button.click()
        except Exception:
            warning("No se encuentra la ventana de notificaciones.")

    def accept_session_cookies(self, save: bool):
        
        if not self.is_logged:
            raise NoLoggedSession('No se puede ejecutar el metodo: accept_session_cookies()')
        
        self.wait()
        try:
            accept_button = self.browser_handler.find_element(By.XPATH, SAVE_SCOOKIES_XPATH)
            no_accept_button = self.browser_handler.find_element(By.XPATH, DONT_SAVE_SCOOKIES_XPATH)
            if save:
                accept_button.click()
            else:
                no_accept_button.click()
        except Exception:
            warning("No se encuentra la ventana de permanencia.")
        finally:
            self.save_cookies('ig_{}'.format(self.username))
            self.wait()
        

    def login(self, sv_cookies: bool=False, accept_nt: bool=False):
        
        if not self.__is_in_page:
            raise PageNotLoaded(IG_URL)
        if self.is_logged:
            warning('login(): No se puede iniciar sesion porque ya se ha iniciado sesion con una cuenta, debe cerrar sesion primero.')
            return
        
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

        self.accept_notifications(False)
    
    def search_for(self, searching:str):

        if not self.is_logged:
            raise NoLoggedSession("No se pueden buscar cuentas si no se ha iniciado sesion con una cuenta previamente.")
        
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
        if not self.is_logged:
            raise NoLoggedSession('logout(): No se puede cerrar una sesion si no se ha iniciado sesion antes.')
        self.username = ''
        self.pwd = ''
        #Elimina las cookies de sesion que estan cargadas (si es que las hay)
        self.delete_cookies()
        self.is_logged = False


    def close(self):
        try:
            self.logout()
        except NoLoggedSession:
            #print("sesion abierta: "+self.is_logged)
            pass
        self.close_browser_handler()
        

    
    def follow_by_hashtag(self, hashtag: str) -> list[str]:
        """
    #       :follow_by_Hashtag(max_follow: int, hashatg: str) -> list[str]:

            Funcion para seguir cuentas aleatorias a partir de los likes 
            de un post aleatorio obtenido de un determinado hashtag.

            Hay que tener cuidado a la hora de especificar el max_follow, ya que
            instagram tiene un limite de 60 seguidas por hora y 150 por dia.

            retorna la lista de cuentas seguidas.
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
            #Espera hasta que cargue la seccion de informacion de la cuenta (Seguidos, Seguidores, etc)
            locator = (By.CSS_SELECTOR, f'ul[class="{AC_INFO_SECTION_CLASSES}"]')
            WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located(locator))
            
            followers_link = self.browser_handler.find_element(By.CSS_SELECTOR, f'li[class="{AC_FOLLOWERS_LINK_CLASSES}"]:nth-child(2)')
            followers_link.click()
            self.wait()

            #Reduce el tamaño de la ventana para que aparezca la scroll bar y asi poder actualizar la lista de seguidores
            #   ya que por algun motivo que desconozco al bajar la scroll bar del widget de la lista de seguidores hasta el final
            #   esta lista no se actualiza y solo se actualiza cuando estoy en el final y subo y bajo el scroll bar de la ventana de la pagina.
            self.browser_handler.set_window_size(412, 400)
            self.browser_handler.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            #falta el codigo para seguir la lista de cuentas

        except NoSuchElementException as e:
            warning(f"follow_by_hashtag(): no se encuentra el link para ver seguidores de la cuenta.:{e}")

        return account_list
#<------------------------------><------------------------------><------------------------------>
    
class UrbanVpn:
    
    def __init__(self,
                 browser: Browser | IgBot,
                 country: str,
                 #ad_block: bool,
                 #anti_phish: bool
                 ):
        self.browser = browser
        if not self.browser.use_vpn:
            raise BrowserVpnNotEnable()
        self.browser_handler = self.browser.browser_handler
        self.country = country
        #self.ad_block = ad_block
        #self.anti_phish = anti_phish
        self.__is_in_page = False

        
    def init_page(self, preload_cookies:bool=True):
        self.browser_handler.implicitly_wait(4)
        if preload_cookies:
            try:
                self.browser.load_cookies('vpn')
            except CookiesDontExists:
                warning('No existen cookies para el vpn')
        self.browser_handler.get(URBAN_VPN_LINK)
        self.__is_in_page = True
        WebDriverWait(self.browser_handler, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'promotion__text')))
        self.accept_terms()
    
    def accept_terms(self):

        try:
            terms_button = self.browser_handler.find_element(By.CLASS_NAME, 'consent-text-controls__action')
            terms_button.click()
            self.browser.wait()
            #self.browser.save_cookies('vpn')
        except NoSuchElementException:
            #warning('no cargo la pagina para aceptar terminos')
            pass
        

    def activate(self):
        
        if not self.__is_in_page:
            raise PageNotLoaded(URBAN_VPN_LINK)
        try:
            country_input =  WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
            country_input.send_keys(self.country)

            run_button = self.browser_handler.find_element(By.CLASS_NAME, 'play-button--play')
            run_button.click()

            #WebDriverWait(self.browser_handler, WAIT_MAX).until(EC.presence_of_element_located((By.CLASS_NAME, 'play-button--pause')))
        except NoSuchElementException:
            print('No se encontraron')

    def close(self):
        self.__is_in_page = False
    

def main():
    bot = IgBot()
    bot.username = 'darkm31'

    bot.init_ig()
    bot.accept_notifications(False)
    #bot.search_for('#programacionvenezuela')
    bot.follow_by_hashtag('#programacionvenezuela')
    time.sleep(100000)

    bot.close()

if __name__ == "__main__":
    main()
