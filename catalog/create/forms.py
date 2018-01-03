from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class CreateItemForm(Form):
    category = StringField('category', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField(label='description', validators=[DataRequired()])
    submit = SubmitField("Send")
