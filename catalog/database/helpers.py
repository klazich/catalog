import random

from sqlalchemy.exc import IntegrityError, OperationalError
from mimesis import Personal, Text, Food, Business, Internet, Generic, Games, Address, UnitSystem, Development, Hardware

from catalog.database import metadata, engine, session
from catalog.models import Item, Category, User

address = Address('en')
business = Business('en')
development = Development('en')
food = Food('en')
games = Games('en')
hardware = Hardware('en')
internet = Internet('en')
personal = Personal('en')
text = Text('en')
unit_system = UnitSystem('en')


class C:
    city = address.city
    company = business.company
    cpu = hardware.cpu
    dish = food.dish
    drink = food.drink
    emoji = internet.emoji
    game = games.game
    home_page = internet.home_page
    programming_language = development.programming_language
    state = address.state
    subreddit = internet.subreddit
    unit = unit_system.unit

    def __get




def populate_categories():
    categories = []
    for k in cat_subs:
        category = Category(name=k.replace('_', ' '))
        categories.append(category)

    session.add_all(categories)
    session.commit()


def populate_users(count=100):
    used = set()
    users = []
    for _ in range(count):
        name = personal.name()
        while name in used:
            name = personal.name()
        email = personal.email()
        while email in used:
            email = personal.email()
        picture = personal.avatar()
        while picture in used:
            picture = personal.avatar()

        used.update([name, email, picture])

        users.append(User(name=name, email=email, picture=picture))

    session.add_all(users)
    session.commit()


def populate_items(count=600):
    categories = session.query(Category).all()
    users = session.query(User).all()

    used = set()
    items = []

    for _ in range(count):
        user = random.choice(users)
        category = random.choice(categories)
        category_key = category.name.replace(' ', '_')
        func = cat_subs[category_key].__getattribute__(category_key)

        name = func()
        while name in used:
            name = func()
        used.add(name)

        item = Item(
            name=name,
            description=text.text(),
            category=category,
            user=user)

        items.append(item)

    session.add_all(items)
    session.commit()


def populate():
    populate_categories()
    populate_users()
    print('annnnnnd items...')
    populate_items()


def populate_item(count=200, locale='en'):
    food = Food(locale=locale)
    text = Text(locale=locale)

    users = session.query(User).all()
    categories = session.query(Category).all()

    if not users:
        populate_user()
        users = session.query(User).all()
    if not categories:
        populate_category()
        categories = session.query(Category).all()

    for _ in range(count):
        category = categories[random.randrange(0, len(categories))]
        user = users[random.randrange(0, len(users))]

        item = Item(
            name=food.__getattribute__(category.name)(),
            description=text.text(),
            user=user,
            category=category)

        session.add(item)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


def populate_category():
    for name in ['dish', 'drink', 'fruit', 'spices', 'vegetable']:
        category = Category(name=name)

        session.add(category)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


def populate_user(count=75, locale='en'):
    person = Personal(locale=locale)

    for _ in range(count):
        user = User(
            name=person.full_name(),
            email=person.email(),
            picture=person.avatar())

        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


def init_db():
    print('Creating tables from metadata...')
    metadata.create_all(bind=engine)
    print('  done')


def drop_db():
    print('Dropping tables from metadata...')
    metadata.drop_all(bind=engine)
    print('  done')


def populate_db():
    print('Populating the database...')
    print('  category table...')
    populate_category()
    print('  user table...')
    populate_user()
    print('  item table...')
    populate_item()
    print('  done')


def reload_db():
    drop_db()
    init_db()
    populate_db()
