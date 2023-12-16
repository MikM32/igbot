
class UncompatibleDefaultBrowser(Exception):

    def __init__(self, browser_name: str):

        self.msg = "El navegador {} no es compatible con el bot. Debe usar Chrome o Firefox".format(browser_name)
        super().__init__(self.msg)

class NotInitizalizedHandler(Exception):

    def __init__(self, handler: any):

        self.msg = " El Handler no ha sido inicializado."
        super().__init__(self.msg)