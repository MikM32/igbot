from winreg import HKEY_CURRENT_USER, HKEY_CLASSES_ROOT, OpenKey, QueryValueEx

def get_browser_name() -> str:
    register_path = r'Software\Microsoft\Windows\Shell\Associations\UrlAssociations\https\UserChoice'
    with OpenKey(HKEY_CURRENT_USER, register_path) as key:
        return str(QueryValueEx(key, "ProgId")[0])

""" obtiene solo el directiorio del navegador (ignora argumentos y comillas dobles)"""    
def format_path(s:str) -> str:
    res=''
    for char in s[1:]:
        if char == '"':
            return res
        else:
            res+=char

""" Obtiene el directorio completo del ejecutable del navegador predeterminado"""
def get_browser_exepath() -> str:
    browser = get_browser_name()
    register_path = r'{}\shell\open\command'.format(browser)
    fullpath = ''
    with OpenKey(HKEY_CLASSES_ROOT, register_path) as key:
        cmd = str(QueryValueEx(key, "")[0]) #Obtiene el comando que ejecuta al navegador predeterminado del registro
        fullpath = format_path(cmd)
    return fullpath
