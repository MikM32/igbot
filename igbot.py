""" Bot de Instagram """
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.firefox.service import Service as FService
import default_browser

def get_webdriver_path(browser_type: str) -> str:
    webdriver_path="webdrivers\\"

    if "Chrome" in browser_type:
        webdriver_path+= "chromedriver.exe"
    elif "Firefox" in browser_type:
        webdriver_path+= "geckodriver.exe"
    else:
        raise Exception("Navegador predeterminado no soportado")
    
    return webdriver_path

class IgBot:

    def __init__(self, default_browser: bool=True, *args):
        
        self.def_browser = default_browser.get_browser_exepath()
        if(default_browser):
            self.webdriver_path = get_webdriver_path(self.def_browser)
        else:
            self.webdriver_path = args[0]

        self.browser_handler = None
        self.options = None
        self.service = None

        if "Chrome" in self.def_browser:
            self.options = COptions()
            self.options.binary_location = self.webdriver_path
            self.service = CService(executable_path=self.def_browser)
            self.browser_handler = webdriver.Chrome(options=self.options, service=self.service)
        elif "Firefox" in self.def_browser:
            self.options = FOptions()
            self.options.binary = self.webdriver_path
            self.service = FService(executable_path=self.def_browser)
            self.browser_handler = webdriver.Firefox(options=self.options, service=self.service)
        else:
            raise Exception("Navegador predeterminado no soportado")
        
    def close_browser_handler(self):
        self.browser_handler.quit()



def main():
    bot = IgBot()

if __name__ == "__main__":
    main()
