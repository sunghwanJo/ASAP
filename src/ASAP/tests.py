import unittest, json, struct
from socket import AF_INET, SOCK_STREAM, socket

HOST='127.0.0.1'
PORT=9338

class Client(object):
    def __init__(self, host, port):
        self.cs = socket(AF_INET, SOCK_STREAM)
        self.cs.connect((host, port))
        
    
    def request(self, request_data):
        request_data = json.dumps(request_data)
        self.cs.send('%d\n'%len(request_data))
        self.cs.send(request_data)
        recved = self.cs.recv(15)
        print '>>>',recved
        index = recved.find('\n')
        response_length = int(recved[:index])
        result = '%s%s'%(recved[recved.find('\n')+1:], self.cs.recv(response_length-len(recved)+1+index))
        return json.loads(result)


class TestBasic(unittest.TestCase):
    def test_connection(self):
        cs = socket(AF_INET, SOCK_STREAM)
        result = cs.connect_ex((HOST, PORT))
        cs.close()
        self.assertEqual(result, 0)

    def test_basic_protocol(self):
        c = Client(HOST, PORT)
        data = c.request({'test':123})
        self.assertTrue(data.has_key('status'))
        self.assertTrue(data['status'].has_key('code'))
        self.assertTrue(data['status'].has_key('reason'))
        self.assertEqual(data['status']['code'], 'NoParameterError')
        self.assertEqual(data['status']['reason'], 'protocol')
        self.assertTrue(data.has_key('protocol'))
        self.assertEqual(data['protocol'], '')

if __name__ == '__main__':
    unittest.main()
