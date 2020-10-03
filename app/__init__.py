"""App initialisation"""
# pylint: disable=import-error
from flask import Flask

from config import Config


APP = Flask(__name__)
APP.config.from_object(Config)

from app import errors  # pylint: disable=wrong-import-position
from app import routes
