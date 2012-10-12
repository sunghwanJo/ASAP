from ASAP.exceptions import NoParameterError
from ASAP import settings
from threading import Thread
import json, datetime
            

class Request(object):
    _conn = None
    parameters = None
    meta = None
    response = None
    
    def __init__(self, conn, parameters):
        self._conn = conn        
        self.parameters = parameters 
        self.meta = dict()
        self.meta['request_time'] = str(datetime.datetime.now()) 
    
    def get_parameter(self, key, is_required=True):
        value = self.parameters.get(key, None)
        if value == None and is_required:
            raise NoParameterError(key)
        return value
    
    def reply(self, response):
        self.response = response
        response = json.dumps(response)
        self._conn.send('%s\n'%len(response))
        self._conn.send(response)
        self.meta['response_time'] = str(datetime.datetime.now())
    
    def is_replied(self):
        return self.response != None

class RequestProcessor(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request
    
    def run(self):
        response = dict(protocol='')
        traced_back = ''
        try:
            response['protocol'] = self.request.get_parameter('protocol')
            import navigator
            reload(navigator)
            from navigator import Navigator
            view = Navigator.get_view(self.request.get_parameter('protocol'))
            return_dict = view(self.request)
            if type(return_dict) == dict:
                response.update(view(self.request))
        except Exception, exception:
            response['status'] = dict(code=str(exception.__class__.__name__), reason=unicode(exception))
            import traceback
            traced_back = traceback.format_exc()
        else:
            response['status'] = dict(code='OK', reason='OK')
            
        self.request.reply(response)
        self.log(traced_back)
    
    def log(self, traced_back):
        if settings.DEBUG:
            from log import Logger
            logger = Logger(self.request, traced_back)
            logger.log()

class Connection(Thread):
    default_protocols=['university_list']
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    
    def run(self):
        self.send_default_info()
        while True:
            request = self.get_request()
            if not request:
                self.conn.close()
                break
            request_processor = RequestProcessor(request)
            request_processor.start()
    
    def get_request(self):
        recved = self.conn.recv(15)
        if recved:
            print [ord(x) for x in recved]
            index = recved.find('\n')
            response_length = int(recved[:index])
            parameters = '%s%s'%(recved[recved.find('\n')+1:], self.conn.recv(response_length-len(recved)+1+index))
            print parameters
            parameters = json.loads(parameters)
            return Request(self.conn, parameters)

    def send_default_info(self):
         for protocol in self.default_protocols:
            parameters = dict(protocol=protocol)
            request_processor = RequestProcessor(Request(self.conn, parameters))
            request_processor.start()
