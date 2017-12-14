from slugify import slugify
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from catalog.database import Base


class Model(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class Item(Model):
    __tablename__ = 'item'

    title = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String(250), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='items')

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='items')

    def __init__(self, title, description, user, category=None):
        self.title = title
        self.description = description
        self.user = user
        self.category = category
        self.slug = slugify(self.title)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user': self.user.name,
            'category': self.category.name
        }

    def __repr__(self):
        return '<Item: {} in {}>'.format(self.title, self.category.name)


class Category(Model):
    __tablename__ = 'category'

    name = Column(String(250), nullable=False)
    slug = Column(String(250), nullable=False)

    items = relationship('Item', order_by=Item.title, back_populates='category')

    def __init__(self, name, items=None):
        if items is None:
            items = []
        self.name = name
        self.items = items
        self.slug = slugify(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [
                i.serialize() for i in self.items
            ]
        }

    def __repr__(self):
        return '<Category: {}>'.format(self.name)


class User(Model):
    __tablename__ = 'user'

    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    slug = Column(String(250), nullable=False)
    picture = Column(String(250))

    items = relationship('Item', order_by=Item.id, back_populates='user')

    def __init__(self, name, email, items=None, picture=None):
        if items is None:
            items = []
        self.name = name
        self.email = email
        self.picture = picture
        self.items = items
        self.slug = slugify(self.name)

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

    def __repr__(self):
        return '<User: {} {}>'.format(self.name, self.email)
