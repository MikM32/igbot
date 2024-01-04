
class UncompatibleDefaultBrowser(Exception):

    def __init__(self, browser_name: str):

        self.msg = "El navegador {} no es compatible con el bot. Debe usar Chrome o Firefox".format(browser_name)
        super().__init__(self.msg)

class NotInitizalizedHandler(Exception):

    def __init__(self):

        self.msg = " El Handler no ha sido inicializado."
        super().__init__(self.msg)

class CookiesDontExists(Exception):

    def __init__(self, social_pre: str):

        self.msg = "No se pueden cargar las cookies para {} porque no existen en el directorio 'galletas'.".format(social_pre.upper())
        super().__init__(self.msg)

class InstagramBadPassword(Exception):

    def __init__(self):
        self.msg = "La password ingresada es incorrecta."
        super().__init__(self.msg)

class InvalidInputData(Exception):

    def __init__(self):
        self.msg = "El usuario o la password ingresada son invalidos."
        super().__init__(self.msg)

class NoLoggedSession(Exception):

    def __init__(self, aditional_msg: str=''):
        self.msg = "No se ha iniciado sesion con una cuenta. {}".format(aditional_msg)
        super().__init__(self.msg)

class ResultsNotFound(Exception):

    def __init__(self, search:str):
        self.msg = "No se encontraron resultados para la busqueda: {}.".format(search)
        super().__init__(self.msg)

class PageNotLoaded(Exception):
    def __init__(self, page:str):
        self.msg = "No se ha cargado la pagina: {}.".format(page)
        super().__init__(self.msg)

class IgUsernameNotFound(Exception):
    def __init__(self):
        self.msg = "Falta el nombre de usuario de instagram."
        super().__init__(self.msg)

class BrowserVpnNotEnable(Exception):
    def __init__(self):
        self.msg = "No se habilito el vpn para este navegador."
        super().__init__(self.msg)
        
def warning(msg:str):
    print(f"Advertencia!: {msg}")