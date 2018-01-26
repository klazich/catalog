import random

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from mimesis import Generic

from .models import metadata, Item, Category, User
from config import config_obj

engine = create_engine(config_obj['default'].DATABASE_URI)
metadata.create_all(bind=engine)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)

g = Generic('en')


class UniqueRandomDatabaseData:
    def __init__(self):
        self._mimesis_category_funcs = [
            g.address.city, g.address.state, g.business.company, g.development.programming_language, g.food.dish,
            g.food.drink, g.games.game, g.hardware.cpu, g.internet.emoji, g.internet.home_page, g.internet.subreddit,
            g.science.chemical_element, g.transport.car, g.unit_system.unit]
        self._used_item_names = set()
        self._used_user_email = set()

    def item(self):
        func = random.choice(self._mimesis_category_funcs)
        category_name = func.__name__
        item_name = func()
        if item_name in self._used_item_names:
            category_name, item_name = self.item()
        self._used_item_names.add(item_name)
        return category_name, item_name

    def user(self):
        user_email = g.personal.email()
        user_name = g.personal.name()
        if user_email in self._used_user_email:
            user_email, user_name = self.user()
        self._used_user_email.add(user_email)
        return user_email, user_name

    def categories(self):
        return [func.__name__ for func in self._mimesis_category_funcs]


def init_db():
    print(' creating tables from metadata...', end='')
    metadata.create_all(bind=engine)
    print('done')


def drop_db():
    print(' dropping tables from metadata...', end='')
    metadata.drop_all(bind=engine)
    print('done')


def populate_db():
    print()
    drop_db()
    init_db()
    users = populate_users()
    categories = populate_categories()
    items = populate_items()
    print('\nCommitted to database:\n'
          '  {} users\n'
          '  {} categories\n'
          '  {} items'.format(len(users), len(categories), len(items)))


def populate_users(n=100):
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
    print(' populating items table..........', end='')
    fake = UniqueRandomDatabaseData()
    users = session.query(User).all()
    categories = {c.name: c for c in session.query(Category).all()}
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
