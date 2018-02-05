import random
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import metadata, Item, Category, User
from config import config_obj

# create engine and bind the metadata tables from catalog.models.py
engine = create_engine(config_obj['default'].DATABASE_URI)
metadata.create_all(bind=engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)


def drop_db():
    """Drops all database tables"""
    print('dropping tables from metadata')
    metadata.drop_all(bind=engine)
    print('...done')


def init_db():
    """Creates all database tables"""
    print('creating tables from metadata')
    metadata.create_all(bind=engine)
    print('...done')
