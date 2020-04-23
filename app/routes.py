from flask import render_template, request, jsonify
from app import app
from app.forms import MessageFieldsForm
from app.parser import Parser
from app.geo_code import GeoCode


@app.route("/")
def index():
    """Landing page"""
    form = MessageFieldsForm()
    return render_template("index.html", form=form)


@app.route("/process", methods=["POST"])
def process():
    """Process page"""

    content = ""
    status_code = 404

    if "message" in request.form:
        # Parse the user input
        parser = Parser()
        parsed_message = parser.parse(request.form["message"])

        content = parsed_message["content"]
        status_code = parsed_message["status_code"]

        if status_code < 400:
            # Send the parsed input to the geo code api
            geo_code = GeoCode()
            geo_response = geo_code.api_request(parsed_message["content"])

            content = geo_response["content"]
            status_code = geo_response["status_code"]

            if status_code < 400:
                pass

    return jsonify(content=content, status_code=status_code)
