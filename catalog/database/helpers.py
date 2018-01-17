import random

from mimesis import Generic
from sqlalchemy.exc import IntegrityError

from catalog.database import metadata, engine, Session
from catalog.models import Item, Category, User

g = Generic('en')


def populate_db():
    drop_db()
    init_db()
    p = Populate()
    items = p.build()
    add_item_objects(items)


def init_db():
    print('creating tables from metadata...', end='')
    metadata.create_all(bind=engine)
    print('done')


def drop_db():
    print('cropping tables from metadata...', end='')
    metadata.drop_all(bind=engine)
    print('done')


def add_item_objects(items):
    print('committing data to database...', end='')
    session = Session()
    session.add_all(items)

    try:
        session.commit()
    except IntegrityError as err:
        session.rollback()
        session.close()
        print('failed')
        print('removing slug collisions...', end='')
        items = _remove_slug_collisions(items, err.params[2])
        print(len(items))
        print('done')
        print('trying commit again...', end='')
        session = Session()
        session.add_all(items)
        session.commit()

    session.close()
    print('done')


class Populate:
    def __init__(self, user_count=150, item_count=600):
        self.categories = {}
        self.users = {}
        self.unique_emails = list(_generate_unique_emails(user_count))
        self.unique_category_items = _generate_unique_category_items(item_count)

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


def _random_category_item():
    func = random.choice([
        g.address.city, g.address.state, g.business.company, g.development.programming_language, g.food.dish,
        g.food.drink, g.games.game, g.hardware.cpu, g.internet.emoji, g.internet.home_page, g.internet.subreddit,
        g.science.chemical_element, g.transport.car, g.unit_system.unit
    ])
    return func.__name__, func()


def _generate_unique_category_items(n):
    category_items = set()
    while len(category_items) < n:
        category_items.add(_random_category_item())
    return category_items


def _generate_unique_emails(n):
    emails = set()
    while len(emails) < n:
        emails.add(g.personal.email.__call__())
    return emails


def _remove_slug_collisions(items, bad_slug):
    print(bad_slug)
    culprits = list(filter(lambda x: x.slug == bad_slug, items))
    rest = set(items) - set(culprits)
    return list(rest)
