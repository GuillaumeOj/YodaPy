import requests
import json
from urllib.parse import quote

from flask import Response
from app import app


class GeoCode:
    def __init__(self):
        self.geo_token = app.config["GEO_TOKEN"]
        self.geo_url = app.config["GEO_URL"]

    def api_request(self, query_text):
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
                content = max(locations, key=lambda location: location["relevance"])
            else:
                status_code = 404

        content = json.dumps(content, indent=4)
        return Response(response=content, mimetype="application/json", status=status_code)
