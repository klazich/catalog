from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from catalog.models import metadata
from config import config_obj

engine = create_engine(config_obj['default'].DATABASE_URI)
metadata.create_all(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
