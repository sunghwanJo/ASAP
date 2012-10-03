'''
Created on 2012. 10. 3.

@author: Anonymous
'''
from ASAP.network import Connection
from socket import AF_INET, SOCK_STREAM, socket

class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket(AF_INET, SOCK_STREAM)
    
    def start_server(self):
        self.s.bind((self.host, self.port))
        self.s.listen(1)
        while True:
            try:
                conn, addr = self.s.accept()
                request_acceptor = Connection(conn, addr)
                request_acceptor.start()
            except Exception, e:
                print e

if __name__ == '__main__':
    server = Server('0.0.0.0', 9338)
    server.start_server()
