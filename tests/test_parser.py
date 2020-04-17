from app.parser import Parser


class TestParser:
    def test_lower_text(self):
        parser = Parser('Test and Retest!')
        expected_result = 'test and retest!'
        parser.lower_text()
        assert parser.question == expected_result

    def test_remove_accents(self):
        parser = Parser('éùéî')
        expected_result = 'euei'
        parser.remove_accents()
        assert parser.question == expected_result

    def test_split_sentences(self):
        parser = Parser('First sentence. And a question? Wonderfull!')
        expected_result = ['First sentence', 'And a question', 'Wonderfull']
        parser.split_sentences()
        assert parser.question == expected_result

    def test_find_question(self):
        parser = Parser(
            '''Salut Yoda, comment vas-tu ? Peux-tu me dire où trouver la tour Eiffel ?
            Passes un bonne journée !'''
        )
        expected_result = 'Peux-tu me dire où trouver la tour Eiffel'
        parser.find_question()
        assert parser.question == expected_result

    def test_find_location(self):
        parser = Parser(
            '''Salut Yoda, comment vas-tu ? Peux-tu me dire où trouver la tour Eiffel ?
            Passes un bonne journée !'''
        )
        expected_result = 'tour Eiffel'
        parser.find_location()
        assert parser.question == expected_result
