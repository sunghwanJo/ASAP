'''
Created on 2012. 10. 3.

@author: Anonymous
'''
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from navigator import Navigator
import json

class RequestAcceptor(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    
    def run(self):
        print self.addr
        received_data = self.get_data()
        navigator = Navigator(received_data)
        response = navigator.get_response()
        print response
        self.conn.send(response)
        
    
    def get_data(self):
        data = []
        while True:
            fragment = self.conn.recv(10240)
            data.append(fragment)
            try:
                result = json.loads(''.join(data))
                break
            except:
                pass
        return result
            

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
                request_acceptor = RequestAcceptor(conn, addr)
                request_acceptor.start()
            except Exception, e:
                print e

if __name__ == '__main__':
    server = Server('0.0.0.0', 9338)
    server.start_server()
