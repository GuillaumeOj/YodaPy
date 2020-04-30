import requests
from urllib.parse import urljoin, quote

from flask import Response

from app import app


class WikiSearch:
    """WikiSearch.
    Search articles around geographics coordinates."""

    def __init__(self):
        self.wiki_api_url = app.config["WIKI_API_URL"]
        self.wiki_url = app.config["WIKI_URL"]

    def search_article(self, query_text):
        """Get articles near coordinates and return one choose randomly."""
        # Query parameters
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
                # Keep only one article choosen randomly
                content = min(articles, key=lambda article: article["index"])

                # Build an url for getting the article
                encoded_url = quote(content["title"])
                article_url = urljoin(self.wiki_url, encoded_url)
                content["url"] = article_url

        return content
