import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated = Column(DateTime, onupdate=datetime.datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='items')

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='items')

    def __repr__(self):
        return '<Item {} in {}>'.format(self.title, self.category.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created': self.created,
            'updated': self.updated,
            'user': self.user.name,
            'category': self.category.name
        }


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    items = relationship('Item', order_by=Item.id, back_populates='user')

    def __repr__(self):
        return '<User {} {}>'.format(self.name, self.email)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture,
            'items': [
                i.serialize() for i in self.items
            ]
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    items = relationship('Item', order_by=Item.title, back_populates='category')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [
                i.serialize() for i in self.items
            ]
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
