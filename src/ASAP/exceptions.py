class ASAPError(Exception):
    def __init__ (self, message):
        import inspect
        self.caller = inspect.stack()[2]
        self.message = message

    def __str__ (self):
        return self.message
    

class NoParameterError(ASAPError):
    pass