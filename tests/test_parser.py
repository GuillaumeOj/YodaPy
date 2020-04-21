from app.parser import Parser


class TestParser:

    parser = Parser()

    def test_lower_text(self):
        TestParser.parser._user_input = 'Test and Retest!'
        TestParser.parser.lower_text()
        expected_result = 'test and retest!'
        assert TestParser.parser._lower_input == expected_result

    def test_remove_accents(self):
        TestParser.parser._lower_input = 'éùéî'
        TestParser.parser.remove_accents()
        expected_result = 'euei'
        assert TestParser.parser._unaccented_input == expected_result

    def test_split_sentences(self):
        TestParser.parser._unaccented_input = 'First sentence. And a question? Wonderfull!'
        TestParser.parser.split_sentences()
        expected_result = ['First sentence', 'And a question', 'Wonderfull']
        assert TestParser.parser._sentences == expected_result

    def test_find_question(self):
        TestParser.parser._sentences = [
            'salut yoda, comment vas',
            'tu',
            'peux',
            'tu me dire ou trouver la tour eiffel',
            'passes une bonne journee'
        ]
        TestParser.parser.find_question()
        expected_result = 'tu me dire ou trouver la tour eiffel'
        assert TestParser.parser._question == expected_result

    def test_clear_question(self):
        TestParser.parser._question = 'tu me dire ou trouver la tour eiffel'
        TestParser.parser.clear_question()
        expected_result = 'tour eiffel'
        assert TestParser.parser._parsed_question == expected_result
