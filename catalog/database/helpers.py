import random
import mimesis

from sqlalchemy.exc import IntegrityError, OperationalError
from mimesis import Personal, Text, Food, Business, Internet, Generic, Games, Address, UnitSystem, Development, \
    Hardware, helpers

from catalog.database import metadata, engine, session
from catalog.models import Item, Category, User

address = Address('en')
food = Food('en')
games = Games('en')
personal = Personal('en')
text = Text('en')

g = Generic('en')

c_map = {
    'city': g.address.city,
    'company': g.business.company,
    'cpu': g.hardware.cpu,
    'dish': g.food.dish,
    'drink': g.food.drink,
    'emoji': g.internet.emoji,
    'game': g.games.game,
    'home page': g.internet.home_page,
    'programming language': g.development.programming_language,
    'state': g.address.state,
    'subreddit': g.internet.subreddit,
    'unit': g.unit_system.unit
}


def pop():
    drop_db()
    init_db()
    populate_categories()
    populate_users()


def populate_categories():
    session.add_all([Category(name=n) for n in c_map])
    session.commit()


def populate_users(count=100):
    names = set()
    while len(names) < count:
        names.add(g.personal.name())
    emails = set()
    while len(emails) < count:
        emails.add(g.personal.email())
    pictures = set()
    while len(pictures) < count:
        pictures.add(g.personal.avatar())

    while all([names, emails, pictures]):
        session.add(User(
            name=names.pop(),
            email=emails.pop(),
            picture=pictures.pop()
        ))

    session.commit()


def populate_items(count=600):
    users = session.query(User).all()
    categories = session.query(Category).all()
    used = set()

    for n in range(count):

        category = random.choice(categories)
        name = c_map[category.name]()
        while name in used:
            name = c_map[category.name]()
            print('(looping)', name)
        used.add(name)

        print(n, category.name, name)

        session.add(Item(
            name=name,
            description=g.text.text(),
            category=category,
            user=random.choice(users)
        ))

        if n % 20 == 0:
            print('     committing @', n)
            session.commit()

    session.commit()


# def populate_items(count=600):
#     categories = session.query(Category).all()
#     users = session.query(User).all()
#
#     used = set()
#     items = []
#
#     for _ in range(count):
#         user = random.choice(users)
#         category = random.choice(categories)
#         category_key = category.name.replace(' ', '_')
#         func = cat_subs[category_key].__getattribute__(category_key)
#
#         name = func()
#         while name in used:
#             name = func()
#         used.add(name)
#
#         item = Item(
#             name=name,
#             description=text.text(),
#             category=category,
#             user=user)
#
#         items.append(item)
#
#     session.add_all(items)
#     session.commit()


# def populate():
#     populate_categories()
#     populate_users()
#     print('annnnnnd items...')
#     populate_items()


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
