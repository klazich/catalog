from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired


class CreateItemForm(FlaskForm):
    category = SelectField(
        'category name')

    new_category = StringField(
        'category name',
        render_kw={'placeholder': 'enter category name'})

    name = StringField(
        'item name',
        validators=[InputRequired()],
        render_kw={'placeholder': 'enter item name'})

    description = TextAreaField(
        'item description',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Enter item description'})

    submit = SubmitField()
