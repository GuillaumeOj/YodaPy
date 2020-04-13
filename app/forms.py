from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class MessageFieldsForm(FlaskForm):
    message = TextAreaField('Your message')
    submit = SubmitField('Send')
