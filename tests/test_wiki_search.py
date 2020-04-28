from app.wiki_search import WikiSearch


class TestWikiSearch:
    def test_search_article(self, monkeypatch):
        articles = [
            {
                "index": 3,
                "title": "Buste de Gustave Eiffel par Antoine Bourdelle",
                "extract": "Ceci est un extrait",
            },
            {
                "index": 1,
                "title": "Tour Eiffel",
                "extract": "Ceci est un autre extrait qui devrait sortir de la méthode.",
            },
            {
                "index": 2,
                "title": "Le Jules Verne",
                "extract": "Ceci est le dernier extrait",
            },
        ]

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

        result = WikiSearch().search_article("query_text").get_json()

        assert result == articles[1]
