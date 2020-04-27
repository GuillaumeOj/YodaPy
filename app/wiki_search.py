import requests
import json
from urllib.parse import urljoin, quote
from random import choice


from flask import Response

from app import app


class WikiSearch:
    """WikiSearch.
    Search articles around geographics coordinates."""

    def __init__(self):
        self.wiki_api_url = app.config["WIKI_API_URL"]
        self.wiki_url = app.config["WIKI_URL"]

    def geodata_request(self, query_coordinates: list) -> object:
        """Get articles near coordinates and return one choose randomly.

        Parameters
        ----------
        query_coordinates : list
            query_coordinates

        Returns
        -------
        object

        """
        parameters = {
            "action": "query",
            "format": "json",
            "list": "geosearch",
            "gscoord": f"{query_coordinates[0]}|{query_coordinates[1]}",
        }

        response = requests.get(self.wiki_api_url, params=parameters)

        articles = []
        content = {}

        # Return the nearest article if response is ok
        if response.ok:
            articles = response.json()["query"]["geosearch"]

            articles = [
                {
                    "pageid": article["pageid"],
                    "title": article["title"],
                    "dist": article["dist"],
                }
                for article in articles
            ]

            if articles:
                status_code = response.status_code
                # Keep only one article choosen randomly
                # content = min(articles, key=lambda article: article["dist"])
                content = choice(articles)
            else:
                status_code = 404

        # Return the result as an HTTP response with a JSON body
        content = json.dumps(content, indent=4)
        return Response(response=content, mimetype="application/json", status=status_code)

    def text_request(self, pageid: int) -> object:
        """Get the introduction for a specific article using his id.

        Parameters
        ----------
        pageid : int
            pageid

        Returns
        -------
        object

        """
        parameters = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "explaintext": True,
            "exchars": 250,
            "pageids": pageid,
            "exintro": True,
        }

        response = requests.get(self.wiki_api_url, params=parameters)

        text = []
        content = {}

        # Return the intro of the article if response is ok
        if response.ok:
            text = response.json()["query"]["pages"][str(pageid)]

            content = {
                "title": text["title"],
                "extract": text["extract"].replace("\n", ""),
            }

            # Build an url for getting the article
            encoded_url = quote(content["title"])
            article_url = urljoin(self.wiki_url, encoded_url)
            content["url"] = article_url

        # Return the result as an HTTP response with a JSON body
        content = json.dumps(content, indent=4)
        return Response(
            response=content, mimetype="application/json", status=response.status_code
        )
