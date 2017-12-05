import datetime
import random

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError

from catalog.database import Base, db_session


class Model(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class Item(Model):
    __tablename__ = 'item'

    # id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    # created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    # updated = Column(DateTime, onupdate=datetime.datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='items')

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='items')

    def __init__(self, title, description, user, category=None):
        self.title = title
        self.description = description
        self.user = user
        self.category = category

    def __repr__(self):
        return '<Item {} in {}>'.format(self.title, self.category.name)

    @staticmethod
    def bootstrap(count=500, locale='en'):
        from mimesis import Food, Text
        food = Food(locale=locale)
        text = Text(locale=locale)

        users = db_session.query(User).all()
        categories = db_session.query(Category).all()

        if not users:
            User.bootstrap()
            users = db_session.query(User).all()
        if not categories:
            Category.bootstrap()
            categories = db_session.query(Category).all()

        for _ in range(count):
            category = categories[random.randrange(0, len(categories))]
            user = users[random.randrange(0, len(users))]

            item = Item(
                title=food.__getattribute__(category.name)(),
                description=text.text(),
                user=user,
                category=category
            )

            db_session.add(item)
            try:
                db_session.commit()
            except IntegrityError:
                db_session.rollback()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            # 'created': self.created,
            # 'updated': self.updated,
            'user': self.user.name,
            'category': self.category.name
        }


class Category(Model):
    __tablename__ = 'category'

    # id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    items = relationship('Item', order_by=Item.title, back_populates='category')

    def __init__(self, name, items=None):
        if items is None:
            items = []
        self.name = name
        self.items = items

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    @staticmethod
    def bootstrap():
        for name in ['dish', 'drink', 'fruit', 'spices', 'vegetable']:
            category = Category(name=name)

            db_session.add(category)
            try:
                db_session.commit()
            except IntegrityError:
                db_session.rollback()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [
                i.serialize() for i in self.items
            ]
        }


class User(Model):
    __tablename__ = 'user'

    # id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    picture = Column(String(250))

    items = relationship('Item', order_by=Item.id, back_populates='user')

    def __init__(self, name, email, items=None, picture=None):
        if items is None:
            items = []
        self.name = name
        self.email = email
        self.picture = picture
        self.items = items

    def __repr__(self):
        return '<User {} {}>'.format(self.name, self.email)

    @staticmethod
    def bootstrap(count=75, locale='en'):
        from mimesis import Personal
        person = Personal(locale=locale)

        for _ in range(count):
            user = User(
                name=person.full_name(),
                email=person.email(),
                picture=person.avatar()
            )

            db_session.add(user)
            try:
                db_session.commit()
            except IntegrityError:
                db_session.rollback()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'items': [
                i.serialize for i in self.items
            ]
        }
