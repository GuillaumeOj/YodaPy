import unicodedata
import os.path
import json
import string

current_dir = os.path.abspath(os.path.dirname(__file__))


class Parser:
    def __init__(self, question):
        self.question = question

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

        # Extend the stopwords' list with the keyword
        self.stopwords.extend(self.keywords)

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
            if character in string.punctuation:
                sentences.append(self.question[start:i].strip())
                start = i + 1
        if sentences:
            self.question = sentences
        else:
            self.question = [self.question]

    def find_question(self):
        self.split_sentences()

        user_question = ''

        for keyword in self.keywords:
            for sentence in self.question:
                if keyword in sentence:
                    user_question = sentence

        self.question = user_question

    def clear_question(self):

        # Find the question
        self.find_question()

        # Clean the question
        clean_question = self.question.split()

        for word in clean_question:
            if word in self.stopwords:
                clean_question.remove(word)

        self.question = ' '.join(clean_question)
