import requests
from app import app


class GeoCode:
    def __init__(self):
        self.geo_token = app.config["GEO_TOKEN"]
        self.geo_url = app.config["GEO_URL"]
        self.query_text = ""

    def api_request(self, query_text):
        self.query_text = query_text
        url = f"{self.geo_url}/{self.query_text}.json"
        parameters = {
            "access_token": self.geo_token,
        }

        response = requests.get(url, params=parameters)

        features = []

        # Return a list of features if response is ok
        if response.ok:
            features = response.json()["features"]

            return (
                [
                    {
                        "relevance": feature["relevance"],
                        "text": feature["text"],
                        "place_name": feature["place_name"],
                        "center": feature["center"],
                    }
                    for feature in features
                ],
                response.status_code,
            )

        # Return the http status code else
        return ([], response.status_code)
