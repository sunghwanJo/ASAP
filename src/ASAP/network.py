from ASAP.navigator import Navigator
from ASAP.exceptions import NoParameterError
from ASAP import settings
from threading import Thread
import json, datetime, struct
            

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
        self._conn.send(struct.pack(">I", len(response)))
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
            view = Navigator.get_view(self.request.get_parameter('protocol'))
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
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    
    def run(self):
        while True:
            request = self.get_request()
            if not request:
                continue
            request_processor = RequestProcessor(request)
            request_processor.start()
    
    def get_request(self):
        recved = self.conn.recv(4)
        if recved:
            print [ord(x) for x in recved]
            request_data_length = struct.unpack(">I", recved)[0]
            recved = self.conn.recv(request_data_length)
            print ">>>",recved
            parameters = json.loads(recved)
            return Request(self.conn, parameters)
