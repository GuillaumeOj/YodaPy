import os.path
import json
from random import choice

from app import app

current_dir = os.path.abspath(os.path.dirname(__file__))


class Bot:
    """Used for generate text from the bot"""

    def __init__(self):
        json_path = os.path.join(current_dir, "static/json/yoda.json")
        with open(json_path) as json_file:
            self.bot_dict = json.load(json_file)

    def random_choice(self, dict_key):
        """Return a random choice in a dict"""
        choosen_message = choice(self.bot_dict[dict_key])
        choosen_message = {"bot_message": choosen_message}

        return choosen_message

    def random_error(self, dict_key):
        """Return a random choice in a dict"""
        choosen_error = choice(self.bot_dict[dict_key])
        choosen_error = {"bot_error": choosen_error}

        return choosen_error

    @property
    def hello(self):
        """Say hello!"""
        message = self.random_choice("hello")
        message["bot_message"] += "\n"
        message["bot_message"] += self.instructions["bot_message"]

        return message

    @property
    def instructions(self):
        """Return the bot instructions"""
        message = {"bot_message": "\n".join(self.bot_dict["instructions"])}

        return message

    @property
    def found_place(self):
        """Return a bot message if a place is found"""
        return self.random_choice("found_place")

    @property
    def found_article(self):
        """Return an bot message if an article was found"""
        return self.random_choice("found_article")

    @property
    def error(self):
        """Return an error message"""
        return self.random_error("error")

    @property
    def not_found(self):
        """Return a not found message"""
        return self.random_error("not_found")

    @property
    def parse_error(self):
        """Return a parser error message"""
        return self.random_error("parse_error")
