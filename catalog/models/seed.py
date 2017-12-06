import random

from sqlalchemy.exc import IntegrityError
from mimesis import Personal, Text, Food

from catalog.models import Item, Category, User
from catalog import db


def populate_item(count=200, locale='en'):
    food = Food(locale=locale)
    text = Text(locale=locale)

    users = db.session.query(User).all()
    categories = db.session.query(Category).all()

    if not users:
        populate_user()
        users = db.session.query(User).all()
    if not categories:
        populate_category()
        categories = db.session.query(Category).all()

    for _ in range(count):
        category = categories[random.randrange(0, len(categories))]
        user = users[random.randrange(0, len(users))]

        item = Item(
            title=food.__getattribute__(category.name)(),
            description=text.text(),
            user=user,
            category=category
        )

        db.session.add(item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def populate_category():
    for name in ['dish', 'drink', 'fruit', 'spices', 'vegetable']:
        category = Category(name=name)

        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def populate_user(count=75, locale='en'):
    person = Personal(locale=locale)

    for _ in range(count):
        user = User(
            name=person.full_name(),
            email=person.email(),
            picture=person.avatar()
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
