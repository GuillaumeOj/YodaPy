from app.parser import Parser


class TestParser:
    PARSER = Parser()

    def test_lower_text(self, monkeypatch):
        self.PARSER._parsed_input = "Test and Retest!"
        self.PARSER.lower_text()
        result = self.PARSER._parsed_input
        assert result == "test and retest!"

    def test_remove_accents(self):
        self.PARSER._parsed_input = "éùéî"
        self.PARSER.remove_accents()
        result = self.PARSER._parsed_input
        assert result == "euei"

    def test_split_sentences(self):
        self.PARSER._parsed_input = "First sentence. And a question? Wonderfull!"
        self.PARSER.split_sentences()
        result = self.PARSER._parsed_input
        assert result == ["First sentence", "And a question", "Wonderfull"]

    def test_find_question(self):
        self.PARSER._parsed_input = [
            "salut yoda, comment vas",
            "tu",
            "peux",
            "tu me dire ou trouver la tour eiffel",
            "passes une bonne journee",
        ]
        self.PARSER.find_question()
        result = self.PARSER._parsed_input
        assert result == "tu me dire ou trouver la tour eiffel"

    def test_clear_question(self):
        self.PARSER._parsed_input = "tu me dire ou trouver la tour eiffel"
        self.PARSER.clear_question()
        result = self.PARSER._parsed_input
        assert result == "tour eiffel"
