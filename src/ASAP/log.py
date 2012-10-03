from ASAP import settings
from ASAP.exceptions import IllegalStateError

class Logger(object):
    def __init__(self, request, traced_back):
        if not request.is_replied():
            raise IllegalStateError('Logger cannot be initilized because request is not replied')
        self.request = request     
        self.log_content = {
                'Time': {'Request Time':self.request.meta['request_time'], 'Response Time':self.request.meta['response_time']},
                'Request':self.request.parameters,
                'Response':self.request.response,
                'Error':'\n%s'%traced_back
               }
    
    def get_log_str(self, key, value):
        import json
        if type(value) in (dict, list, tuple):
            value = '\n%s\n'%json.dumps(value, indent=4)
        return '%s : %s'%(key, value)
    
    def log(self):
        f = file(settings.LOG_FILE_PATH, 'a')
        f.write('\n\n%s\n'%('='*70))        
        for key in ['Request', 'Response', 'Time', 'Error']:
            f.write(self.get_log_str(key, self.log_content[key]))
        f.close()