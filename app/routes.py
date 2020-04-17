from flask import render_template, request
from app import app
from app.forms import MessageFieldsForm
from app.parser import Parser


@app.route('/')
def index():
    """Landing page"""
    form = MessageFieldsForm()
    return render_template('index.html', form=form)


@app.route('/process', methods=['POST'])
def process():
    """Process page"""
    if 'message' in request.form:
        parsed_message = Parser(request.form['message']).parse
        return parsed_message
