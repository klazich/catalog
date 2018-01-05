from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, RadioField, SelectField
from wtforms.validators import InputRequired

from catalog.database import Session
from catalog.models import Category


class CreateCategoryForm(FlaskForm):
    categories = SelectField(
        'category name',
        choices=[(c.name, c.name) for c in Session.query(Category).all()],
        render_kw={'placeholder': 'choose a category'})

    new_category = StringField(
        'category name',
        render_kw={'placeholder': 'enter category name'})

    submit = SubmitField()


class CreateItemForm(CreateCategoryForm):
    # new_category = StringField(
    #     'create new category',
    #     render_kw={'placeholder': 'Create New Category'})
    # categories = SelectField(
    #     'choose category',
    #     choices=[(c.name, c.name) for c in Session.query(Category).all()] + [('new_category', 'new category')],
    #     render_kw={"placeholder": "Category Name"})

    name = StringField(
        'item name',
        validators=[InputRequired()],
        render_kw={'placeholder': 'enter item name'})

    description = TextAreaField(
        'item description',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Enter item description'})

    submit = SubmitField()
