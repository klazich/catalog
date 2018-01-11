from flask_restless import APIManager

from catalog.database import session
from catalog.models import Item, Category

manager = APIManager(session=session)

# Item JSON endpoint
# /api/items/[<int:id>]
manager.create_api(Item)

# Category JSON endpoint
# /api/categories/[<int:id>]
manager.create_api(Category)
