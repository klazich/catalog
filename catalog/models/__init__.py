from slugify import slugify
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship
from flask_login import UserMixin

from catalog.database import Base
from catalog import login_manager, db_session


class Model(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime(timezone=True), default=func.current_timestamp(timezone=True))
    date_updated = Column(DateTime(timezone=True), default=func.current_timestamp(timezone=True),
                          onupdate=func.current_timestamp(timezone=True))


class Item(Model):
    __tablename__ = 'items'

    name = Column(String(250), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    slug = Column(String(250), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='items')

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='items')

    def __init__(self, name, description, user, category=None):
        self.name = name
        self.description = description
        self.user = user
        self.category = category
        self.slug = slugify(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user': self.user.name,
            'category': self.category.name
        }

    def __repr__(self):
        return '<Item: {} in {}>'.format(self.name, self.category.name)


class Category(Model):
    __tablename__ = 'categories'

    name = Column(String(250), nullable=False, unique=True)
    slug = Column(String(250), nullable=False)

    items = relationship('Item', order_by=Item.name, back_populates='category')

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


class User(UserMixin, Model):
    __tablename__ = 'users'

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
        return '<User: {}({})>'.format(self.name, self.email)


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).filter_by(int(user_id) == User.id).first()
