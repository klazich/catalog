import random

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from mimesis import Generic

from .models import metadata, Item, Category, User
from config import config_obj

# create engine and bind the metadata tables from catalog.models.py
engine = create_engine(config_obj['default'].DATABASE_URI)
metadata.create_all(bind=engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)

g = Generic('en')


class UniqueRandomDatabaseData(object):
    """
    For creating Item, Category and User objects. Used in populating functions.

    :type _mimesis_category_funcs: list[() -> str]
    :type _used_item_names: set[str]
    :type _used_user_email: set[str]
    """

    def __init__(self):
        # an array of mimesis functions used to populate tables
        self._mimesis_category_funcs = [
            g.address.city, g.address.state, g.business.company,
            g.development.programming_language, g.food.dish, g.food.drink, g.games.game,
            g.hardware.cpu, g.internet.emoji, g.internet.home_page, g.internet.subreddit,
            g.science.chemical_element, g.transport.car, g.unit_system.unit]

        # Used to keep item names unique and avoid IntegrityError SQLAlchemy exceptions
        self._used_item_names = set()

        # Used to keep user emails unique and avoid IntegrityError SQLAlchemy exceptions
        self._used_user_email = set()

    def item(self):
        """
        Returns a category name and a unique item name in that category for item creation.

        :return: a tuple of category name and item name
        :rtype: (str, str)
        """
        func = random.choice(self._mimesis_category_funcs)
        category_name = func.__name__
        item_name = func()
        if item_name in self._used_item_names:
            category_name, item_name = self.item()
        self._used_item_names.add(item_name)
        return category_name, item_name

    def user(self):
        """
        Returns a unique email address and random name for user creation.

        :return: a tuple of user email and user name
        :rtype: (str, str)
        """
        user_email = g.personal.email()
        user_name = g.personal.name()
        if user_email in self._used_user_email:
            user_email, user_name = self.user()
        self._used_user_email.add(user_email)
        return user_email, user_name

    def categories(self):
        """
        Returns a list of the category names in _mimesis_category_funcs.

        :return: a list of category names
        :rtype: list[str]
        """
        return [func.__name__ for func in self._mimesis_category_funcs]


def drop_db():
    """Drops all database tables"""
    print(' dropping tables from metadata...', end='')
    metadata.drop_all(bind=engine)
    print('done')


def init_db():
    """Creates all database tables"""
    print(' creating tables from metadata...', end='')
    metadata.create_all(bind=engine)
    print('done')


def populate_db():
    """
    Calls functions in this module to populate a database.

    :return: a tuple of lists of Item types, Category types and User types
    :rtype: (list[Item], list[Category], list[User])
    """
    print()
    drop_db()
    init_db()
    users = populate_users()
    categories = populate_categories()
    items = populate_items()
    print('\nCommitted to database:\n'
          '- {} users\n'
          '- {} categories\n'
          '- {} items'.format(len(users), len(categories), len(items)))
    return items, categories, users


def populate_users(n=100):
    """
    Creates *n* users of type User with unique emails and commits them the User
    table (Defaults to n=100).

    Note: Needs to be called before populate_items otherwise, populate_items may raise
          an exception.

    :param n: count of users to create
    :type n: int
    :return: a list of User objects of length *n*
    :rtype: list[User]
    """
    print(' populating users table..........', end='')
    fake = UniqueRandomDatabaseData()
    users = []
    while len(users) < n:
        user_email, user_name = fake.user()
        user_picture = g.personal.avatar()
        users.append(User(
            name=user_name,
            email=user_email,
            picture=user_picture))
    session.add_all(users)
    session.commit()
    print('done')
    return users


def populate_categories():
    """
    Creates a list of category objects from UniqueRandomDatabaseData.categories and commits them
    to the Category table.
    :return: a list of Category objects
    :rtype: list[Category]
    """
    print(' populating categories table.....', end='')
    fake = UniqueRandomDatabaseData()
    categories = []
    for category_name in fake.categories():
        categories.append(Category(
            name=category_name.replace('_', ' ')))
    session.add_all(categories)
    session.commit()
    print('done')
    return categories


def populate_items(n=600):
    """
    Creates a list of Item objects with unique names of length *n* and commits them to
    the Item table.

    Note: populate_users and populate_categories should be called before this function
          otherwise, this may raise an exception.

    :param n: count of items to create
    :type n: int
    :return: a list of Item objects of length *n*
    :rtype: list[Item]
    """
    print(' populating items table..........', end='')
    fake = UniqueRandomDatabaseData()
    users = session.query(User).all()  # all users from database
    categories = {c.name: c for c in session.query(
        Category).all()}  # all categories from database
    items = []
    while len(items) < n:
        item_category_name, item_name = fake.item()
        item_description = g.text.text()
        item_user = random.choice(users)
        item_category = categories[item_category_name.replace('_', ' ')]
        items.append(Item(
            name=item_name,
            description=item_description,
            category=item_category,
            user=item_user))
    session.add_all(items)
    session.commit()
    print('done')
    return items
