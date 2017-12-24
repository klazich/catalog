import random
import string

from flask import make_response
from flask.views import MethodView
from flask import session as flask_session

from catalog import Session
from catalog.models import User


class UserAPI(MethodView):
    def get(self, user_id: object = None) -> User:
        if user_id:
            # expose a single user
            pass
        else:
            # return a list of users
            pass

    def post(self):
        # create a new user
        pass

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass
