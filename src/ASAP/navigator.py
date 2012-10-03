from ASAP.request import Request
import json

class Navigator(object):
    response = {}
    def __init__(self, parameters):        
        try:
            self.request = Request(parameters)
        except Exception, exception:
            self.response['status'] = dict(code=str(exception.__class__.__name__), reason=unicode(exception))
        else:
            self.response['status'] = dict(code='OK', reason='OK')
            
    def get_response(self):        
        return json.dumps(self.response)