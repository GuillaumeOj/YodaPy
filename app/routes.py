import json

from flask import render_template, request, jsonify, Response

from app import app
from app.forms import MessageFieldsForm

from app.parser import Parser
from app.geo_code import GeoCode
from app.wiki_search import WikiSearch
from app.bot import Bot

bot = Bot()


@app.route("/", methods=["GET"])
def index():
    """Landing page"""
    form = MessageFieldsForm()
    return render_template("index.html", form=form)


@app.route("/process", methods=["POST"])
def process():
    """Process the user input"""

    content = {}

    if "message" in request.form and ":help" in request.form["message"]:
        # Display instructions if the user type :help
        content = bot.instructions
    elif "message" in request.form:
        # Parse the user input
        parser = Parser()
        parser_response = parser.parse(request.form["message"])

        if "parsed_input" in parser_response:
            # Send the parsed input to the geo code api
            geo_code = GeoCode()
            geo_response = geo_code.api_request(parser_response["parsed_input"])

            if "place_name_fr" in geo_response:
                status_code = 200
                content["map"] = geo_response
                content["map"].update(bot.found_place)

                # Send the coordinates to wikipedia
                wiki_search = WikiSearch()
                wiki_response = wiki_search.geo_search_article(
                    content["map"]["latitude"], content["map"]["longitude"]
                )

                if "url" in wiki_response:
                    content["article"] = wiki_response
                    content["article"].update(bot.found_article)
            else:
                content = bot.not_found
        else:
            content = bot.parse_error

    return jsonify(content)


@app.route("/hello", methods=["GET"])
def hello():
    """Say hello to user and send instructions"""

    content = bot.hello

    return jsonify(content)


@app.route("/error", methods=["GET"])
def bot_error():
    """Error message from the bot"""

    content = bot.error

    return jsonify(content)
