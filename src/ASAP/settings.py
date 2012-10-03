import os

HOST = '0.0.0.0'
PORT = 9338

DEBUG = True

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
LOG_FILE_PATH = os.path.join(PROJECT_PATH, 'log', 'log.txt')