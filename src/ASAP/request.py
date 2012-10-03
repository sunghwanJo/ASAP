from ASAP.exceptions import NoParameterError
class Request(object):
    def __init__(self, parameters):        
        self.parameters = parameters        
        self.protocol = self.get_parameter('protocol')
    
    def get_parameter(self, key, is_required=True):
        value = self.parameters.get(key, None)
        if value == None and is_required:
            raise NoParameterError(key)
        return value
        