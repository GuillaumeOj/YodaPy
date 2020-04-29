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

        if parser_response.status_code == 200:
            # Send the parsed input to the geo code api
            geo_code = GeoCode()
            geo_response = geo_code.api_request(parser_response.get_json())

            if geo_response.status_code == 200:
                content["map"] = geo_response.get_json()

                # Send the coordinates to wikipedia
                wiki_search = WikiSearch()

                wiki_page = wiki_search.search_article(content["map"]["text"])
                if wiki_page.status_code == 200:
                    content["article"] = wiki_page.get_json()

    if content:
        status_code = 200
    else:
        status_code = 404

    content = json.dumps(content, indent=4)
    return Response(response=content, mimetype="application/json", status=status_code)


@app.route("/hello", methods=["GET"])
def hello():
    """Hello page"""

    content = Bot().hello

    if content:
        status_code = 200
    else:
        status_code = 404

    content = json.dumps(content, indent=4)
    return Response(response=content, mimetype="application/json", status=status_code)
