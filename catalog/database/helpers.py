import random

from sqlalchemy.exc import IntegrityError
from mimesis import Personal, Text, Food

from catalog.database import metadata, engine, session
from catalog.models import Item, Category, User


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
            category=category
        )

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
            picture=person.avatar()
        )

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
