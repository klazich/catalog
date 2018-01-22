from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Model(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())


class Item(Model):
    __tablename__ = 'items'

    name = Column(String(250), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='items')

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='items')

    def __init__(self, name, description, category, user):
        self.name = name.lower()
        self.description = description
        self.user = user
        self.category = category

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user': self.user.name,
            'category': self.category.name}

    def __repr__(self):
        return '<Item: {}>'.format(self.name)


class Category(Model):
    __tablename__ = 'categories'

    name = Column(String(250), nullable=False, unique=True)

    items = relationship('Item', order_by=Item.name, back_populates='category')

    def __init__(self, name, items=None):
        if items is None:
            items = []
        self.name = name.lower()
        self.items = items

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [i.serialize for i in self.items]}

    def __repr__(self):
        return '<Category: {}>'.format(self.name)


class User(Model):
    __tablename__ = 'users'

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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'items': [i.serialize for i in self.items]}

    def __repr__(self):
        return '<User: {}>'.format(self.name)
