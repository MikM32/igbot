""" Bot de Instagram """
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.firefox.service import Service as FService
from selenium.webdriver.common.by import By
import default_browser
import time, random
from constants import *

def get_webdriver_path(browser_type: str) -> str:
    webdriver_path= WEBDRIVER_PATH

    if "Chrome" in browser_type:
        webdriver_path+= "chromedriver.exe"
    elif "Firefox" in browser_type:
        webdriver_path+= "geckodriver.exe"
    else:
        raise Exception("Navegador predeterminado no soportado")
    
    return webdriver_path

class IgBot:

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

        if "Chrome" in self.def_browser:
            self.options = COptions()
            #self.options.add_argument("--user-data-dir={}".format(CHROME_USER_DATA))
            self.options.add_argument('--profile-directory=Default')
            self.options.binary_location = self.def_browser
            self.service = CService(executable_path=self.webdriver_path)
            self.browser_handler = webdriver.Chrome(options=self.options, service=self.service)
        elif "Firefox" in self.def_browser:
            self.options = FOptions()
            self.options.binary = self.def_browser
            self.service = FService(executable_path=self.webdriver_path)
            self.browser_handler = webdriver.Firefox(options=self.options, service=self.service)
        else:
            raise Exception("Navegador predeterminado no soportado")
    
    def init_ig_main(self):
        self.browser_handler.implicitly_wait(5)
        self.browser_handler.get(IG_URL)

    def login(self, user:str, pwd:str):
        self.wait()
        username_input = self.browser_handler.find_element(By.XPATH, USER_INPUT_XPATH)
        pwd_input = self.browser_handler.find_element(By.XPATH, PWD_INPUT_XPATH)

        username_input.send_keys(user)
        pwd_input.send_keys(pwd)

        login_button = self.browser_handler.find_element(By.XPATH, LOGIN_BUTTON_XPATH)
        login_button.click()

        self.wait()
    
    def wait(self):
        self._update_sleep_secs()
        time.sleep(self.sleep_secs)

    def _update_sleep_secs(self):
        self.sleep_secs = random.randint(5, 12)

    def close_browser_handler(self):
        self.browser_handler.quit()

 

def main():
    bot = IgBot()
    bot.init_ig_main()
    #bot.login()
    time.sleep(1000)
    bot.close_browser_handler()

if __name__ == "__main__":
    main()
