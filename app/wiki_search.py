import requests
import json
from urllib.parse import urljoin, quote

from flask import Response

from app import app


class WikiSearch:
    """WikiSearch.
    Search articles around geographics coordinates."""

    def __init__(self):
        self.wiki_api_url = app.config["WIKI_API_URL"]
        self.wiki_url = app.config["WIKI_URL"]

    def search_article(self, query_text: str) -> object:
        """Get articles near coordinates and return one choose randomly.

        Parameters
        ----------
        query_text : str
            query_text

        Returns
        -------
        object

        """
        parameters = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": query_text,
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
            articles = response.json()["query"]["pages"]
            articles = list(articles.values())

            # Keep only the data we need
            app.logger.info(articles)
            articles = [
                {
                    "index": article["index"],
                    "title": article["title"],
                    "extract": article["extract"],
                }
                for article in articles
            ]

            if articles:
                status_code = response.status_code
                # Keep only one article choosen randomly
                content = min(articles, key=lambda article: article["index"])
            else:
                status_code = 404

        # Return the result as an HTTP response with a JSON body
        content = json.dumps(content, indent=4)
        return Response(response=content, mimetype="application/json", status=status_code)
