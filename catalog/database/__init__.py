from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from catalog.models import metadata
from config import config

engine = create_engine(config['default'].DATABASE_URI)
metadata.create_all(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
