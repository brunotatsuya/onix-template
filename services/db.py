import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

def inject_service(app):

    @app.service('db')
    class DatabaseService():
        def __init__(self):
            self._conn_str = app.auth.decrypt(os.environ.get('SQLALCHEMY_DATABASE_URI'))
            self.engine = create_engine(self._conn_str)
            self.metadata = MetaData(bind=self.engine)
            self.Base = declarative_base()

        def create_session(self):
            Session = sessionmaker(self.engine)
            return Session()