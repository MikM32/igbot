
class NotInitizalizedHandler(Exception):

    def __init__(self, handler: any):

        self.msg = " El Handler no ha sido inicializado."
        super().__init__(self.msg)