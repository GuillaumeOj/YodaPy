import json
from app.wiki_search import WikiSearch


class TestWikiSearch:
    def test_geodata_request(self, monkeypatch):
        articles = [
            {
                "pageid": 5828872,
                "title": "Buste de Gustave Eiffel par Antoine Bourdelle",
                "dist": 28,
            },
            {"pageid": 1359783, "title": "Tour Eiffel", "dist": 59.5},
            {"pageid": 4641538, "title": "Le Jules Verne", "dist": 63.6},
        ]

        class MockRequestGet:
            def __init__(self, url, params=None):
                self.ok = True
                self.status_code = 200

            def json(self):
                return {
                    "query": {
                        "geosearch": [
                            {
                                "pageid": article["pageid"],
                                "title": article["title"],
                                "dist": article["dist"],
                            }
                            for article in articles
                        ]
                    }
                }

        def mock_random_choice(articles):
            return articles[0]

        monkeypatch.setattr("requests.get", MockRequestGet)

        monkeypatch.setattr("app.wiki_search.choice", mock_random_choice)
        result = WikiSearch().geodata_request("query_text").response
        assert (
            json.loads(WikiSearch().geodata_request("query_text").response[0])
            == articles[0]
        )

    def test_text_request(self, monkeypatch):
        pageid = 5828872
        text = {
            "title": "Buste de Gustave Eiffel par Antoine Bourdelle",
            "extract": "Le buste de Gustave Eiffel par Antoine Bourdelle",
            "url": "https://fr.wikipedia.org/wiki/Buste%20de%20Gustave%20Eiffel%20par%20Antoine%20Bourdelle",
        }

        class MockRequestGet:
            def __init__(self, url, params=None):
                self.ok = True
                self.status_code = 200

            def json(self):
                return {
                    "query": {
                        "pages": {
                            str(pageid): {
                                "title": text["title"],
                                "extract": text["extract"],
                            }
                        }
                    }
                }

        monkeypatch.setattr("requests.get", MockRequestGet)
        assert json.loads(WikiSearch().text_request(pageid).response[0]) == text
