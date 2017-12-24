# from flask_login import login_required

from catalog.database import Session
from catalog.models import Category, Item


def latest_items(limit):
    """
    Helper function that returns the most recent items created
    :param limit: int
    :return: query
    """
    return Session.query(Item).order_by(Item.date_updated).limit(limit)


def get_all_categories():
    """
    Helper function to fetch all category names
    :return: query
    """
    return Session.query(Category).all()


def get_category_by_name(category_name: str) -> Category:
    """
    Get a Category object by its name
    :param category_name: string
    :return: Category
    """
    return Session.query(Category).filter(Category.name == category_name).one_or_none()


def get_category_by_slug(category_slug: str) -> Category:
    """
    Get a Category object by its slugified name
    :param category_slug: string
    :return: Category
    """
    return Session.query(Category).filter(Category.slug == category_slug).one_or_none()


def get_category_by_id(category_id: int) -> Category:
    """
    Get a Category object by its primary id
    :param category_id: int
    :return: Category
    """
    return Session.query(Category).filter(Category.id == category_id).one_or_none()


def get_item_by_title(item_title):
    """
    Get a Item object by its name
    :param item_title: string
    :return: Item
    """
    return Session.query(Item).filter(Item.name == item_title).one_or_none()


def get_item_by_slug(item_slug):
    """
    Get a Item object by its name
    :param item_slug: string
    :return: Item
    """
    return Session.query(Item).filter(Item.slug == item_slug).one_or_none()


def get_item_by_id(item_id):
    """
    Get a Category object by its primary id
    :param item_id: int
    :return: Item
    """
    return Session.query(Item).filter(Item.id == item_id).one_or_none()
