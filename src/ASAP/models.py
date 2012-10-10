#-*-encoding:utf8-*-
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.pool import NullPool
import hashlib

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(64))
    name = db.Column(db.String(30))

    def __init__(self, username, email, password, name=''):
        self.username = username
        self.email = email
        self.password = hashlib.sha256(password)
        self.name = name

    def __repr__(self):
        return '<User %r>'%self.username

    def set_password(self, password):
        self.password = hashlib.sha256(password)


