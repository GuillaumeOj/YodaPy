from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class MessageFieldsForm(FlaskForm):
    message = TextAreaField('Votre message')
    submit = SubmitField('Envoyer')
