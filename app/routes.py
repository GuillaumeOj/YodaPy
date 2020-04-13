from flask import render_template
from app import app
from app.forms import MessageFieldsForm


@app.route("/")
@app.route("/index")
def index():
    messages = [
        {"type": "sent", "content": "Salut Yoda ! Comment tu vas ?"},
        {
            "type": "incoming",
            "content": "Quand 900 ans comme tu auras, moins en forme tu seras",
        },
    ]

    form = MessageFieldsForm()
    return render_template("index.html", messages=messages, form=form)
