"""Config file for the application"""
import os


class Config:  # pylint: disable=too-few-public-methods
    """Configuration"""

    LOGO = "https://img.icons8.com/color/130/000000/baby-yoda.png"
    BOT_NAME = "YodaPy"
    CATCHPHRASE = "Sur YodaPy le bienvenue tu es !"
    AUTHOR = "Guillaume OJARDIAS"

    # To find out which class to use for social links, please see the link below
    # https://www.nerdfonts.com/cheat-sheet
    SOCIAL_LINKS = [
        {
            "profile": True,
            "url": "https://www.linkedin.com/in/guillaume-ojardias-91a46643/",
            "class": "nf-fa-linkedin_square",
        },
        {
            "profile": False,
            "url": "https://github.com/GuillaumeOj",
            "class": "nf-fa-github",
        },
        {
            "profile": False,
            "url": "https://twitter.com/GuillaumeOj",
            "class": "nf-fa-twitter_square",
        },
    ]
    PROFILE_LINK = next(link["url"] for link in SOCIAL_LINKS if link["profile"])

    SECRET_KEY = os.environ.get("SECRET_KEY") or "This-is-my-secret-key"

    # Information about the geo_code API
    # This project use Mapbox https://www.mapbox.com/
    GEO_TOKEN = os.environ.get("GEO_TOKEN") or "This-is-a-foo-tooken"
    PUBLIC_GEO_TOKEN = os.environ.get("PUBLIC_GEO_TOKEN") or "This-is-a-foo-tooken"
    GEO_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"

    # Url for the french wikipedia's API
    WIKI_API_URL = "https://fr.wikipedia.org/w/api.php"
    WIKI_URL = "https://fr.wikipedia.org/wiki/"
