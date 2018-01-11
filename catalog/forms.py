from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional


class ItemForm(FlaskForm):
    category = SelectField(
        'category name',
        validators=[Optional()])

    new_category = StringField(
        'category name',
        validators=[Optional()],
        render_kw={'placeholder': 'enter category name'})

    name = StringField(
        'item name',
        validators=[DataRequired()],
        render_kw={'placeholder': 'enter item name'})

    description = TextAreaField(
        'item description',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Enter item description'})

    submit = SubmitField()
