from app.geo_code import GeoCode


class TestGeoCode:
    def test_api_request(self, monkeypatch):
        locations = [
            {
                "relevance": 1,
                "text_fr": "Tour Eiffel",
                "place_name_fr": "Tour Eiffel, 5 avenue Anatole France, Paris, 75007, France",
                "center": [2.29480075, 48.85878700000001],
            },
            {
                "relevance": 0.899333,
                "text_fr": "Parking Tour Eiffel",
                "place_name_fr": "Parking Tour Eiffel, 75007 Paris, France",
                "center": [2.296247, 48.854961],
            },
            {
                "relevance": 0.496667,
                "text_fr": "France",
                "place_name_fr": "France",
                "center": [2, 47],
            },
        ]

        excepted_result = {
            "relevance": locations[0]["relevance"],
            "text_fr": locations[0]["text_fr"],
            "place_name_fr": locations[0]["place_name_fr"],
            "longitude": locations[0]["center"][0],
            "latitude": locations[0]["center"][1],
        }

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
                            "text_fr": location["text_fr"],
                            "place_name_fr": location["place_name_fr"],
                            "center": location["center"],
                        }
                        for location in locations
                    ]
                }

        monkeypatch.setattr("requests.get", MockRequestGet)
        result = GeoCode().api_request("query_text")
        assert result == excepted_result
