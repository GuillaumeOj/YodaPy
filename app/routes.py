from flask import render_template
from app import app
from app.forms import MessageFieldsForm


@app.route('/')
@app.route('/index')
def index():
    messages = [
        {'type': 'sent', 'content': 'Salut Yoda ! Comment tu vas ?'},
        {
            'type': 'incoming',
            'content': 'Quand 900 ans comme tu auras, moins en forme tu seras',
        },
        {'type': 'sent', 'content': 'Où se trouve OpenClassrooms ?'},
        {'type': 'incoming', 'content': 'A vos intuitions vous fier il faut.',},
        {'type': 'sent', 'content': 'Et plus concrétement ?'},
        {
            'type': 'incoming',
            'content': 'Je ne peux rien lui apprende, cet enfant n\'a aucune patience. Trop de colère en lui, comme son père, il n\'est pas prêt.',
        },
    ]

    form = MessageFieldsForm()
    return render_template('index.html', messages=messages, form=form)
