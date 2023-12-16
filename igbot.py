""" Bot de Instagram """
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.firefox.service import Service as FService
from selenium.webdriver.common.by import By

import default_browser
import time, random
from bot_exceptions import *
from constants import *

def get_webdriver_path(browser_type: str) -> str:
    webdriver_path= WEBDRIVER_ROOT_PATH

    if "Chrome" in browser_type:
        webdriver_path+= "chromedriver.exe"
    elif "Firefox" in browser_type:
        webdriver_path+= "geckodriver.exe"
    else:
        raise Exception("Navegador predeterminado no soportado")
    
    return webdriver_path

class Browser:
    """
        Clase Browser:

        -- atributos:
            -browser_handler: handler del navegador

            -def_browser: cadena que contiene el directorio donde se encuentra el ejecutable del navegador predeterminado

            -options: objeto que contiene los parametros con los cual arrancara el navegador

            -service: objeto que contiene la informacion del webdriver que sera utilizado por el browser_handler

            -sleep_secs: entero que contiene la cantidad de segundos que usara la funcion IgBot.wait()

        -- Metodos:
            -
    """
    def __init__(self, is_def_browser: bool=True, *args: str):
        self.def_browser = default_browser.get_browser_exepath()
        if(is_def_browser):
            self.webdriver_path = get_webdriver_path(self.def_browser)
        else:
            self.webdriver_path = args[0]

        self.browser_handler = None
        self.options = None
        self.service = None
        self.sleep_secs = None

    def _init_chrome(self):
        self.options = COptions()
        #self.options.add_argument("--user-data-dir={}".format(CHROME_USER_DATA))
        self.options.add_argument('--profile-directory=Default')

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
            raise Exception("Navegador predeterminado no soportado")
        
    def wait(self):
        self._update_sleep_secs()
        time.sleep(self.sleep_secs)

    def _update_sleep_secs(self):
        self.sleep_secs = random.randint(5, 12)

    def close_browser_handler(self):
        try:
            if(self.browser_handler == None):
                raise NotInitizalizedHandler(self.browser_handler)
            
            self.browser_handler.quit()
            
        except Exception as e:
            print("No se puede ejecutar el metodo close_browser_handler(): {}".format(e))


class IgBot(Browser):
    """
        Clase IgBot:
            --Metodos:
                -init_if_main(): carga la pagina principal de instagram

                -login(user: str, pwd: str): inicia sesion con una cuenta en instagram 
    """
    def __init__(self, is_def_browser: bool=True, *args: str):
        self.username = None
        super().__init__(is_def_browser, args)
    
    def init_ig_main(self):
        self.browser_handler.implicitly_wait(5)
        self.browser_handler.get(IG_URL)

    def login(self, user:str, pwd:str):
        self.username = user
        self.wait()

        username_input = self.browser_handler.find_element(By.XPATH, USER_INPUT_XPATH)
        pwd_input = self.browser_handler.find_element(By.XPATH, PWD_INPUT_XPATH)

        username_input.send_keys(user)
        pwd_input.send_keys(pwd)

        login_button = self.browser_handler.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
        login_button.click()

        self.wait()


def main():
    bot = IgBot()
    #bot.init_browser_handler()
    #bot.init_ig_main()
    #bot.login()
    #time.sleep(100000)
    bot.close_browser_handler()

if __name__ == "__main__":
    main()
