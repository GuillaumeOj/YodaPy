import json

from flask import render_template, request, jsonify, Response

from app import app
from app.forms import MessageFieldsForm

from app.parser import Parser
from app.geo_code import GeoCode
from app.wiki_search import WikiSearch


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

        if parser_response.status == "200 OK":
            # Send the parsed input to the geo code api
            geo_code = GeoCode()
            geo_response = geo_code.api_request(json.loads(parser_response.response[0]))

            if geo_response.status == "200 OK":
                content["map"] = json.loads(geo_response.response[0])

                # Send the coordinates to wikipedia
                wiki_search = WikiSearch()
                # Invert coordinates between MapBox and Wikipedia
                wiki_coordinates = [
                    content["map"]["center"][1],
                    content["map"]["center"][0],
                ]

                wiki_article_info = wiki_search.geodata_request(wiki_coordinates)

                if wiki_article_info.status == "200 OK":
                    content["article_info"] = json.loads(wiki_article_info.response[0])

                    # Get the content of the article
                    wiki_article = wiki_search.text_request(
                        content["article_info"]["pageid"]
                    )

                    if wiki_article.status == "200 OK":
                        content["article"] = json.loads(wiki_article.response[0])

    if content:
        status_code = 200
    else:
        status_code = 404

    content = json.dumps(content, indent=4)
    return Response(response=content, mimetype="application/json", status=status_code)
