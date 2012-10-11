#-*-coding:utf8-*-
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()

class DatabaseManager(object):
    _instance = None
    _engine = None
    session = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(
                                cls, *args, **kwargs)
            cls._instance.init_database()
        return cls._instance

    def get_engine(self):
        from ASAP import settings
        def main():
            if self._engine:
                return self._engine

            if settings.DATABASE['type'] == 'mysql':
                CONNECTION_STRING, SQLALCHEMY_KWARGS = get_mysql_settings()
            elif settings.DATABASE['type'] == 'sqlite':
                CONNECTION_STRING, SQLALCHEMY_KWARGS = get_sqlite_settings()
            elif settings.DATABASE['type'] == 'other':
                CONNECTION_STRING, SQLALCHEMY_KWARGS = get_other_settings()
            else:
                raise ValueError("DB Type must be either one of mysql, sqlite, or other.")

            engine = db.create_engine(CONNECTION_STRING, **SQLALCHEMY_KWARGS)
            self._engine = engine
            return engine
        def get_mysql_settings():
            CONNECTION_STRING = 'mysql://%s:%s@%s/%s?charset=utf8&use_unicode=1' % \
                (settings.DATABASE['username'],
                 settings.DATABASE['password'],
                 settings.DATABASE['host'],
                 settings.DATABASE['dbname'],
                )
            SQLALCHEMY_KWARGS = {'encoding': 'utf-8',
                                 'convert_unicode': True,
                                 'assert_unicode': False,
                                 'pool_size': 300,
                                 'max_overflow': 10,
                                 'pool_recycle': 5,
                                 'echo_pool': False}
            return CONNECTION_STRING, SQLALCHEMY_KWARGS
        def get_sqlite_settings():
            CONNECTION_STRING = 'sqlite:///%s' % settings.DATABASE['dbname']
            SQLALCHEMY_KWARGS = {'encoding': 'utf-8',
                                 'convert_unicode': True,
                                 'assert_unicode': None,
                                 'poolclass': NullPool}
            return CONNECTION_STRING, SQLALCHEMY_KWARGS
        def get_other_settings():
            CONNECTION_STRING = settings.DATABASE['connection_string']
            SQLALCHEMY_KWARGS = {'encoding': 'utf-8',
                                 'convert_unicode': True,
                                 'assert_unicode': None}
            return CONNECTION_STRING, SQLALCHEMY_KWARGS
        
        return main()



    def init_database(self):
        '''
        Database 와 여기에 접속할 수 있는 Session 을 만든다.
        '''
        
        Base.metadata.create_all(self.get_engine())
        self.session = sessionmaker(bind=self.get_engine(), autoflush=True, autocommit=False)

    def init_test_database(self):
        '''
        TEST 를 위한 Database 를 메모리 상에 만든다. 물론 Session 도.
        '''
        engine = db.create_engine('sqlite://', convert_unicode=True, encoding='utf-8', echo=False)
        self.session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
        Base.metadata.create_all(engine)

    def get_session(self):
        return self.session()
