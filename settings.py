import os

HOST = '0.0.0.0'
PORT = 9338

DEBUG = True

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
LOG_FILE_PATH = os.path.join(PROJECT_PATH, 'log', 'log.txt')

DATABASE = {
    'type':'mysql',#sqlite or mysql or other
    'connection_string':'',#if type is other, requires custom connection string
    'dbname':'oic',#database name for mysql, filename for sqlite
    'username':'oic',#for mysql
    'password':'5wq2MchaJhBYvqLf',#for mysql
    'host':'',#for mysql
}
