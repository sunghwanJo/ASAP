import unittest, json
from socket import AF_INET, SOCK_STREAM, socket

HOST='127.0.0.1'
PORT=9338

class Client(object):
    def __init__(self, host, port):
        self.cs = socket(AF_INET, SOCK_STREAM)
        self.cs.connect((host, port))
        
    
    def request(self, data):
        data = json.loads(data)
        self.cs.send(data)
        return json.loads(self.read(10240))


class TestBasic(unittest.TestCase):
    def test_connection(self):
        cs = socket(AF_INET, SOCK_STREAM)
        result = cs.connect_ex((HOST, PORT))
        cs.close()
        self.assertEqual(result, 0)

    def test_basic_protocol(self):
        c = Client(HOST, PORT)
        data = c.request({})
        self.assertTrue(data.has_key('status'))
        self.assertTrue(data['status'].has_key('code'))
        self.assertTrue(data['status'].has_key('reason'))
        self.assertEqual(data['status']['code'], 'NoParameterError')
        self.assertEqual(data['status']['reason'], 'protocol')

if __name__ == '__main__':
    unittest.main()