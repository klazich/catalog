from flask_restless import APIManager

from catalog.database import session
from catalog.models import Item, Category

manager = APIManager(session=session)

manager.create_api(Item)
manager.create_api(Category)
