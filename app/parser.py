import unicodedata
import os.path
import json

current_dir = os.path.abspath(os.path.dirname(__file__))


class Parser:
    def __init__(self, question):
        self.question = question

    @property
    def parse(self):
        self.lower_text()
        self.remove_accents()
        self.find_question()

        return self.question

    def lower_text(self):
        self.question = self.question.lower()

    def remove_accents(self):
        unicode_text = unicodedata.normalize('NFD', self.question)
        ascii_unaccented = unicode_text.encode('ascii', 'ignore')
        self.question = ascii_unaccented.decode('utf8')

    def split_sentences(self):
        sentences = []
        start = 0
        for i, character in enumerate(self.question):
            if character in '?.!':
                sentences.append(self.question[start:i].strip())
                start = i + 1
        if sentences:
            self.question = sentences
        else:
            self.question = [self.question]

    def find_question(self):
        # Load keaywords for find the question from a json file
        keywords_path = os.path.join(current_dir, 'static/json/question_keywords.json')
        keywords = []
        with open(keywords_path) as json_f:
            keywords = json.load(json_f)

        self.split_sentences()

        user_question = ''

        for keyword in keywords:
            for sentence in self.question:
                if keyword in sentence:
                    user_question = sentence

        self.question = user_question
