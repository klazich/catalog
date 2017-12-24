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
    print('Initializing new database...')
    Base.metadata.create_all(bind=engine)
    print('  done')


def seed_db():
    from catalog.models import seed
    print('Populating the database...')
    print('  ...category table')
    seed.populate_category()
    print('  ...user table')
    seed.populate_user()
    print('  ...item table')
    seed.populate_item()
    print('  done')


def drop_db():
    print('dropping database...')
    Base.metadata.drop_all(bind=engine)
    print('  done')


def reload_db():
    drop_db()
    init_db()
    seed_db()
