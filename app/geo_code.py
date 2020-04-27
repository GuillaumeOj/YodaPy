import requests
import json
from urllib.parse import quote

from flask import Response
from app import app


class GeoCode:
    """GeoCode.
    Send a query to a geocoding api for getting the coordinates of a place"""

    def __init__(self):
        self.geo_token = app.config["GEO_TOKEN"]
        self.geo_url = app.config["GEO_URL"]

    def api_request(self, query_text):
        """api_request.

        :param query_text:
        """

        # Quote the query to avoid any issue
        quoted_query = quote(query_text["parsed_input"])
        url = f"{self.geo_url}/{quoted_query}.json"

        parameters = {
            "access_token": self.geo_token,
        }

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
                status_code = response.status_code
                # Keep only one location in the list with the best relevance
                content = max(locations, key=lambda location: location["relevance"])
            else:
                status_code = 404

        # Return the result as an HTTP response
        content = json.dumps(content, indent=4)
        return Response(response=content, mimetype="application/json", status=status_code)
