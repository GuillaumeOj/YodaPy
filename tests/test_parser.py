from app.parser import Parser


class TestParser:
    PARSER = Parser()

    def test_normalize(self):
        self.PARSER.parsed_input = "Test and Retest! éùéî"
        self.PARSER.normalize()
        result = self.PARSER.parsed_input
        assert result == "test and retest! euei"

    def test_split_sentences(self):
        self.PARSER.parsed_input = "First sentence. And a question? Wonderfull!"
        self.PARSER.split_sentences()
        result = self.PARSER.parsed_input
        assert result == ["First sentence", "And a question", "Wonderfull"]

    def test_find_question(self):
        self.PARSER.parsed_input = [
            "salut yoda, comment vas",
            "tu",
            "peux",
            "tu me dire ou trouver la tour eiffel",
            "passes une bonne journee",
        ]
        self.PARSER.find_question()
        result = self.PARSER.parsed_input
        assert result == "tu me dire ou trouver la tour eiffel"

    def test_clear_question(self):
        self.PARSER.parsed_input = "tu me dire ou trouver la tour eiffel"
        self.PARSER.clear_question()
        result = self.PARSER.parsed_input
        assert result == "trouver tour eiffel"
