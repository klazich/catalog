from os import path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import basedir

Base = declarative_base()

engine = create_engine('sqlite:///{}'.format(path.join(basedir, 'catalog.db')))
Base.metadata.bind = engine

db_session = scoped_session(sessionmaker(bind=engine))


def init_db():
    import catalog.models
    Base.metadata.create_all(bind=engine)


def seed_db():
    from catalog.models import seed
    seed.populate_category()
    seed.populate_user()
    seed.populate_item()


def drop_db():
    Base.metadata.drop_all(bind=engine)
