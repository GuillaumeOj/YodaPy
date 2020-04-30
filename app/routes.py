import json

from flask import render_template, request, jsonify, Response

from app import app
from app.forms import MessageFieldsForm

from app.parser import Parser
from app.geo_code import GeoCode
from app.wiki_search import WikiSearch
from app.bot import Bot


@app.route("/")
def index():
    """Landing page"""
    form = MessageFieldsForm()
    return render_template("index.html", form=form)


@app.route("/process", methods=["POST"])
def process():
    """Process page"""

    content = {}

    if "message" in request.form:
        # Parse the user input
        parser = Parser()
        parser_response = parser.parse(request.form["message"])

        if "parsed_input" in parser_response:
            # Send the parsed input to the geo code api
            geo_code = GeoCode()
            geo_response = geo_code.api_request(parser_response["parsed_input"])

            if "place_name" in geo_response:
                content["map"] = geo_response
                content["map"].update(Bot().answer)

                # Send the coordinates to wikipedia
                wiki_search = WikiSearch()
                wiki_response = wiki_search.search_article(content["map"]["text"])

                if "url" in wiki_response:
                    content["article"] = wiki_response

    if content:
        status_code = 200
    else:
        status_code = 204

    return jsonify(content), status_code


@app.route("/hello", methods=["GET"])
def hello():
    """Hello page"""

    content = Bot().hello

    if content:
        status_code = 200
    else:
        status_code = 204

    return jsonify(content), status_code


@app.route("/error", methods=["GET"])
def bot_error():
    """Error message from the bot"""

    content = Bot().error

    if content:
        status_code = 200
    else:
        status_code = 204

    return jsonify(content), status_code


@app.route("/not_found", methods=["GET"])
def not_found():
    """Not found message from the bot"""

    content = Bot().not_found

    if content:
        status_code = 200
    else:
        status_code = 204

    return jsonify(content), status_code
