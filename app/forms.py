"""Forms from flask"""
# pylint: disable=import-error
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import TextAreaField


class MessageFieldsForm(FlaskForm):
    """User input form"""

    # pylint: disable=too-few-public-methods

    message = TextAreaField("Votre message")
    submit = SubmitField("Envoyer")
