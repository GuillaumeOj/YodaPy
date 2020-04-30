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

    @property
    def hello(self):
        """Say hello!"""
        message = self.bot_dict["hello"]
        message = {"bot_messages": [choice(message)]}

        # Add instructions
        message["bot_messages"].append(self.instructions)

        return message

    @property
    def instructions(self):
        """Return the bot instructions"""
        message = "\n\n".join(self.bot_dict["instructions"])

        return message

    @property
    def wait(self):
        """Return a wait message"""
        message = choice(self.bot_dict["wait"])
        message = {"bot_messages": [message]}

        return message

    @property
    def error(self):
        """Return an error message"""
        message = choice(self.bot_dict["error"])
        message = {"bot_messages": [message]}

        return message
