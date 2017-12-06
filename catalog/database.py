from os import path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


# engine = create_engine('sqlite:///catalog.db')
# db_session = scoped_session(sessionmaker(bind=engine))
#
# Base = declarative_base()
# Base.query = db_session.query_property()
#
#
# def init_db():
#     import catalog.models
#
#     Base.metadata.create_all(bind=engine)


# def seed_db():
#     from catalog.models import seed
#     seed.populate_category()
#     seed.populate_user()
#     seed.populate_item()


class Database:
    def __init__(self, app_dir):
        self.dir = app_dir
        self.engine = create_engine('sqlite:///{}'.format(path.join(self.dir, 'catalog.db')))
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.session.query_property()

    def create(self):
        # import all modules here that might define models so that
        # they will be registered properly on the metadata.  Otherwise
        # you will have to import them first before calling init_db()
        import catalog.models
        self.Base.metadata.create_all(bind=self.engine)

    @staticmethod
    def seed():
        from catalog.models import seed
        seed.populate_category()
        seed.populate_user()
        seed.populate_item()




