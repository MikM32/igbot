
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

        self.msg = "No se pueden cargar las cookies para {} porque no existe en el directorio 'Galletas'.".format(social_pre.upper())
        super().__init__(self.msg)

class InstagramBadPassword(Exception):

    def __init__(self):
        self.msg = "La password ingresada es incorrecta."
        super().__init__(self.msg)