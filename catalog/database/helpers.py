import random
from slugify import slugify

from sqlalchemy.exc import IntegrityError, OperationalError
from mimesis import Personal, Text, Food, Generic

from catalog.database import metadata, engine, session
from catalog.models import Item, Category, User

g = Generic('en')


class Populate:
    def __init__(self, user_count=150, item_count=600):
        self.categories = {}
        self.users = {}
        self.unique_emails = list(self._generate_unique_emails(user_count))
        self.unique_category_items = self._get_unique_category_items(item_count)

    def build(self):
        items = []
        while self.unique_category_items:
            category_name, item_name = self.unique_category_items.pop()
            user_email = random.choice(self.unique_emails)
            items.append(Item(
                name=item_name,
                description=g.text.text(),
                user=self._get_or_new_user(user_email),
                category=self._get_or_new_category(category_name)
            ))
        return items

    def _get_or_new_category(self, category_name):
        if category_name not in self.categories:
            self.categories[category_name] = Category(name=category_name)
        return self.categories[category_name]

    def _get_or_new_user(self, user_email):
        if user_email not in self.users:
            self.users[user_email] = User(
                name=g.personal.name(),
                email=user_email,
                picture=g.personal.avatar()
            )
        return self.users[user_email]

    @staticmethod
    def _generate_unique_emails(n):
        emails = set()
        while len(emails) < n:
            emails.add(g.personal.email.__call__())
        return emails

    @staticmethod
    def _get_unique_category_items(n):
        category_items = set()
        while len(category_items) < n:
            category_items.add(Populate._random_category_item())
        return category_items

    @staticmethod
    def _random_category_item():
        func = random.choice([
            g.address.city, g.address.state, g.business.company, g.development.programming_language, g.food.dish,
            g.food.drink, g.games.game, g.hardware.cpu, g.internet.emoji, g.internet.home_page, g.internet.subreddit,
            g.science.chemical_element, g.transport.car, g.unit_system.unit
        ])
        return func.__name__, func()


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
