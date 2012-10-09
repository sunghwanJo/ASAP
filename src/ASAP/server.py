'''
Created on 2012. 10. 3.

@author: Anonymous
'''
from ASAP.network import Connection
from ASAP.models import DatabaseManager
from ASAP import settings

import os
from socket import AF_INET, SOCK_STREAM, socket

class Server(object):
    def __init__(self, host='', port=0):
        self.prepare_logging()
        DatabaseManager().init_database()
        if host == '':
            host = settings.HOST
        if port == 0:
            port = settings.PORT
        self.host = host
        self.port = port
            
    def prepare_logging(self):
        if settings.DEBUG: 
            os.chdir(settings.PROJECT_PATH)
            if not os.path.exists('log'):
                os.mkdir('log')
                file(settings.LOG_FILE_PATH, 'w').close()
            else:
                if not os.path.exists(settings.LOG_FILE_PATH):
                    file(settings.LOG_FILE_PATH, 'w').close()
        
    
    def start_server(self):               
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((settings.HOST, settings.PORT))
        s.listen(1)
        while True:
            try:
                conn, addr = s.accept()
                request_acceptor = Connection(conn, addr)
                request_acceptor.start()
            except Exception, e:
                print e

if __name__ == '__main__':
    server = Server()
    server.start_server()
