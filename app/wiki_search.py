"""Use the Wikiepedia API"""
from urllib.parse import quote, urljoin

import requests

from app import APP  # pylint: disable=cyclic-import


class WikiSearch:
    """Search articles around geographics coordinates."""

    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.wiki_api_url = APP.config["WIKI_API_URL"]
        self.wiki_url = APP.config["WIKI_URL"]

    def geo_search_article(self, latitude, longitude):
        """Get articles near coordinates and return one choose randomly."""
        # Query parameters
        parameters = {
            "action": "query",
            "format": "json",
            "generator": "geosearch",
            "ggscoord": f"{latitude}|{longitude}",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "exchars": 200,
        }

        response = requests.get(self.wiki_api_url, params=parameters)

        articles = []
        content = {}

        # Return the nearest article if response is ok
        if response.ok:
            articles = response.json()
            if "query" in articles:
                articles = articles["query"]["pages"]
                articles = list(articles.values())

                # Keep only the data we need
                articles = [
                    {
                        "index": article["index"],
                        "title": article["title"],
                        "extract": article["extract"],
                    }
                    for article in articles
                ]

                if articles:
                    # Keep only one article choosen randomly
                    content = min(articles, key=lambda article: article["index"])

                    # Build an url for getting the article
                    encoded_url = quote(content["title"])
                    article_url = urljoin(self.wiki_url, encoded_url)
                    content["url"] = article_url

        return content
