from sqlalchemy import Table

def inject_model(app):

    @app.model('User')
    class User(app.db.Base):
        __table__ = Table('tb_user', app.db.metadata, autoload=True, autoload_with=app.db.engine)