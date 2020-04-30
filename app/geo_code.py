import requests
import json
from urllib.parse import quote

from flask import Response
from app import app


class GeoCode:
    """Send a query to a geocoding api for getting informations about a place."""

    def __init__(self):
        self.geo_token = app.config["GEO_TOKEN"]
        self.geo_url = app.config["GEO_URL"]

    def api_request(self, query_text):
        """Get informations about a place with a query from a user."""
        # Quote the query to avoid any issue
        quoted_query = quote(query_text)
        url = f"{self.geo_url}/{quoted_query}.json"

        parameters = {"access_token": self.geo_token}

        response = requests.get(url, params=parameters)

        features = []
        content = {}

        # Return a list of features if response is ok
        if response.ok:
            features = response.json()["features"]

            locations = [
                {
                    "relevance": feature["relevance"],
                    "text": feature["text"],
                    "place_name": feature["place_name"],
                    "center": feature["center"],
                }
                for feature in features
            ]

            if locations:
                # Keep only one location in the list with the best relevance
                content = max(locations, key=lambda location: location["relevance"])

        return content
