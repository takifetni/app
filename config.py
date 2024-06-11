import os 


class Config:
    SECRET_KEY = os.urandom(24)
    DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'flaskr.sqlite')


