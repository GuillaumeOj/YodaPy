import unicodedata
import os.path
import json
import string

from app import app

current_dir = os.path.abspath(os.path.dirname(__file__))


class Parser:
    def __init__(self):
        self._user_input = ''
        self._lower_input = ''
        self._unaccented_input = ''
        self._sentences = ''
        self._question = ''
        self._parsed_question = ''

        # Load stopwords from a json file
        stopwords_path = os.path.join(current_dir, 'static/json/stopwords.json')
        self.stopwords = []
        with open(stopwords_path) as json_f:
            self.stopwords = json.load(json_f)

        # Load keywords for the question from a json file
        keywords_path = os.path.join(current_dir, 'static/json/question_keywords.json')
        self.keywords = []
        with open(keywords_path) as json_f:
            self.keywords = json.load(json_f)

    def parse(self, user_input):
        self._user_input = user_input

        self.lower_text()
        self.remove_accents()
        self.split_sentences()
        self.find_question()
        self.clear_question()

        return self._parsed_question

    def lower_text(self):
        self._lower_input = self._user_input.lower()

        app.logger.info(f'Lower input => {self._lower_input}')

    def remove_accents(self):
        unicode_text = unicodedata.normalize('NFD', self._lower_input)
        ascii_unaccented = unicode_text.encode('ascii', 'ignore')
        self._unaccented_input = ascii_unaccented.decode('utf8')

        app.logger.info(f'Unaccented input => {self._unaccented_input}')

    def split_sentences(self):
        sentences = []
        start = 0
        for i, character in enumerate(self._unaccented_input):
            if character in '?.!-':
                sentences.append(self._unaccented_input[start:i].strip())
                start = i + 1
        if sentences:
            self._sentences = sentences
        else:
            self._sentences = [self._unaccented_input]

        app.logger.info(f'Sentences => {self._sentences}')

    def find_question(self):
        question = []

        for keyword in self.keywords:
            for sentence in self._sentences:
                if keyword in sentence:
                    question.append(sentence)

        # Keep only the last question
        if question:
            self._question = question[-1]
        else:
            self._question = ''

        app.logger.info(f'Question => {self._question}')

    def clear_question(self):
        splited_question = self._question

        # Replace last punctuations
        for punctuation in string.punctuation:
            if punctuation in splited_question:
                splited_question = splited_question.replace(punctuation, ' ')

        app.logger.info(f'Splitted question => {splited_question}')
        splited_question = splited_question.split()

        # Remove keywords
        for keyword in self.keywords:
            for word in splited_question:
                if keyword in word:
                    splited_question.remove(word)

        app.logger.info(f'New Splitted => {splited_question}')

        parsed_question = []

        # Remove stopwords
        for word in splited_question:
            if word not in self.stopwords and len(word) > 1:
                parsed_question.append(word)

        self._parsed_question = ' '.join(parsed_question)

        app.logger.info(f'Parsed question => {self._parsed_question}')
