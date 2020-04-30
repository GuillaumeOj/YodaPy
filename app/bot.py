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
        choosen_message = {"bot_messages": [choosen_message]}

        return choosen_message

    @property
    def hello(self):
        """Say hello!"""
        message = self.random_choice("hello")

        # Add instructions
        message["bot_messages"].append(self.instructions)

        return message

    @property
    def instructions(self):
        """Return the bot instructions"""
        message = "\n\n".join(self.bot_dict["instructions"])

        return message

    @property
    def answer(self):
        """Return an answer message"""
        return self.random_choice("answer")

    @property
    def error(self):
        """Return an error message"""
        return self.random_choice("error")

    @property
    def not_found(self):
        """Return a not found message"""
        return self.random_choice("not_found")
