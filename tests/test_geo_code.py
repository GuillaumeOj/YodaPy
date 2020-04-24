from app.geo_code import GeoCode


class TestGeoCode:
    def test_api_request(self, monkeypatch):
        locations = [
            {
                "relevance": 1,
                "text": "Tour Eiffel",
                "place_name": "Tour Eiffel, 5 avenue Anatole France, Paris, 75007, France",
                "center": [2.29480075, 48.85878700000001],
            },
            {
                "relevance": 0.899333,
                "text": "Parking Tour Eiffel",
                "place_name": "Parking Tour Eiffel, 75007 Paris, France",
                "center": [2.296247, 48.854961],
            },
            {
                "relevance": 0.496667,
                "text": "France",
                "place_name": "France",
                "center": [2, 47],
            },
        ]

        class MockRequestGet:
            def __init__(self, url, params=None):
                pass
                self.ok = True
                self.status_code = 200

            def json(self):
                return {
                    "features": [
                        {
                            "relevance": location["relevance"],
                            "text": location["text"],
                            "place_name": location["place_name"],
                            "center": location["center"],
                        }
                        for location in locations
                    ]
                }

        monkeypatch.setattr("requests.get", MockRequestGet)
        assert GeoCode().api_request("query_text")["content"] == locations[0]
