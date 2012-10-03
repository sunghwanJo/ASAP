from ASAP.navigator import Navigator
from ASAP.exceptions import NoParameterError
from threading import Thread
import json
            

class Request(object):
    def __init__(self, conn, parameters):
        self._conn = conn        
        self.parameters = parameters        
    
    def get_parameter(self, key, is_required=True):
        value = self.parameters.get(key, None)
        if value == None and is_required:
            raise NoParameterError(key)
        return value
    
    def reply(self, return_dict):
        self._conn.send(json.dumps(return_dict))        

class RequestProcessor(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request
    
    def run(self):
        response = dict(protocol='')
        try:
            response['protocol'] = self.request.get_parameter('protocol')
            view = Navigator.get_view(self.request.get_parameter('protocol'))
            response.update(view(self.request))
        except Exception, exception:
            response['status'] = dict(code=str(exception.__class__.__name__), reason=unicode(exception))
        else:
            response['status'] = dict(code='OK', reason='OK')
        
        self.request.reply(response)

class Connection(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    
    def run(self):
        while True:
            request = self.get_request()
            request_processor = RequestProcessor(request)
            request_processor.start()        
    
    def get_request(self):
        data = []
        while True:
            fragment = self.conn.recv(10240)
            data.append(fragment)
            try:
                parameters = json.loads(''.join(data))
                break
            except:
                pass
        return Request(self.conn, parameters)