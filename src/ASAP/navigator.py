import json

class Navigator(object):
    def __init__(self, request):
        self.request = request
        status = dict(code='OK', reason='OK')
        try:
            protocol = self.request['protocol']
            print protocol
        except KeyError:
            status['code'] = 'NoParameterError'
            status['reason'] = 'protocol'
        self.response = dict(status=status)
        
    
    def get_response(self):        
        return json.dumps(self.response)