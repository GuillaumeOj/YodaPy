from flask import render_template
from app import app
from app.forms import MessageFieldsForm


@app.route('/')
def index():
    """Landing page"""
    form = MessageFieldsForm()
    return render_template('index.html', form=form)
