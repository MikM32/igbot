from winreg import HKEY_CURRENT_USER, HKEY_CLASSES_ROOT, OpenKey, QueryValueEx


def get_chrome_version() -> str:
    register_path = r'SOFTWARE\Google\Chrome\BLBeacon'
    with OpenKey(HKEY_CURRENT_USER, register_path) as key:
        return str(QueryValueEx(key, 'version')[0])
    
def get_browser_name() -> str:
    register_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'
    with OpenKey(HKEY_CURRENT_USER, register_path) as key:
        return str(QueryValueEx(key, "ProgId")[0])

def format_path(s:str) -> str:
    """ obtiene solo el directiorio del navegador (ignora argumentos y comillas dobles)"""  
    return s.split('"')[1]

def get_browser_exepath() -> str:
    """ Obtiene el directorio completo del ejecutable del navegador predeterminado"""
    browser = get_browser_name()
    register_path = r'{}\shell\open\command'.format(browser)
    fullpath = ''
    with OpenKey(HKEY_CLASSES_ROOT, register_path) as key:
        cmd = str(QueryValueEx(key, "")[0]) #Obtiene el comando que ejecuta al navegador predeterminado del registro
        fullpath = format_path(cmd)
    return fullpath

if __name__ == '__main__':
    print(get_chrome_version())
