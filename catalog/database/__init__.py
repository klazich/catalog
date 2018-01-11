from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from catalog.models import metadata
from config import config_obj

engine = create_engine(config_obj['default'].DATABASE_URI)
metadata.create_all(bind=engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)
