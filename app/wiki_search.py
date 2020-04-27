import requests
import json
from urllib.parse import urljoin

from flask import Response

from app import app


class WikiSearch:
    def __init__(self):
        self.wiki_api_url = app.config["WIKI_API_URL"]
        self.wiki_url = app.config["WIKI_URL"]

    def geodata_request(self, query_coordinates):
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
                content = min(articles, key=lambda article: article["dist"])
            else:
                status_code = 404

        content = json.dumps(content, indent=4)

        return Response(response=content, mimetype="application/json", status=status_code)

    def text_request(self, pageid):
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

            # Build an url for the front
            article_url = urljoin(self.wiki_url, content["title"], allow_fragments=False)
            content["url"] = article_url

        # Return the http status code else
        # return {"content": content, "status_code": response.status_code}

        content = json.dumps(content, indent=4)

        return Response(
            response=content, mimetype="application/json", status=response.status_code
        )
