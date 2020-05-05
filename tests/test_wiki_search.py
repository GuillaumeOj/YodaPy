from app.wiki_search import WikiSearch


class TestWikiSearch:
    def test_search_article(self, monkeypatch):
        articles = [
            {
                "index": 3,
                "title": "Buste de Gustave Eiffel par Antoine Bourdelle",
                "extract": "Ceci est un extrait",
                "url": "https://fr.wikipedia.org/wiki/Buste‰20de‰20Gustave%20Eiffel%20par%20Antoine%20Bourdelle",
            },
            {
                "index": 1,
                "title": "Tour Eiffel",
                "extract": "Ceci est un autre extrait qui devrait sortir de la méthode.",
                "url": "https://fr.wikipedia.org/wiki/Tour%20Eiffel",
            },
            {
                "index": 2,
                "title": "Le Jules Verne",
                "extract": "Ceci est le dernier extrait",
                "url": "https://fr.wikipedia.org/wiki/Le%20Jules%20Verne",
            },
        ]

        latitude = 1
        longitude = 1

        class MockRequestGet:
            def __init__(self, url, params=None):
                self.ok = True
                self.status_code = 200

            def json(self):
                return {
                    "query": {
                        "pages": {
                            str(article["index"]): {
                                "index": article["index"],
                                "title": article["title"],
                                "extract": article["extract"],
                            }
                            for article in articles
                        }
                    }
                }

        monkeypatch.setattr("requests.get", MockRequestGet)

        result = WikiSearch().geo_search_article(latitude, longitude)

        assert result == articles[1]
