import unicodedata
import os.path
import json
import string

from app import app

current_dir = os.path.abspath(os.path.dirname(__file__))


class Parser:
    def __init__(self):
        self._user_input = ""
        self._parsed_input = ""

        # Load stopwords from a json file
        stopwords_path = os.path.join(current_dir, "static/json/stopwords.json")
        self.stopwords = []
        with open(stopwords_path) as json_f:
            self.stopwords = json.load(json_f)

        # Load keywords for the question from a json file
        keywords_path = os.path.join(current_dir, "static/json/question_keywords.json")
        self.keywords = []
        with open(keywords_path) as json_f:
            self.keywords = json.load(json_f)

    def parse(self, user_input):
        self._user_input = user_input
        self._parsed_input = self._user_input

        self.lower_text()
        self.remove_accents()
        self.split_sentences()
        self.find_question()
        self.clear_question()

        return self._parsed_input

    def lower_text(self):
        self._parsed_input = self._parsed_input.lower()

    def remove_accents(self):
        unicode_text = unicodedata.normalize("NFD", self._parsed_input)
        ascii_unaccented = unicode_text.encode("ascii", "ignore")
        self._parsed_input = ascii_unaccented.decode("utf8")

    def split_sentences(self):
        sentences = []
        start = 0
        for i, character in enumerate(self._parsed_input):
            if character in "?.!-":
                sentences.append(self._parsed_input[start:i].strip())
                start = i + 1
        if sentences:
            self._parsed_input = sentences
        else:
            self._parsed_input = [self._parsed_input]

    def find_question(self):
        question = []
        for keyword in self.keywords:
            for sentence in self._parsed_input:
                if keyword in sentence:
                    question.append(sentence)

        # Keep only the last question
        if question:
            self._parsed_input = question[-1]
        else:
            self._parsed_input = ""

    def clear_question(self):
        splited_question = self._parsed_input

        # Replace last punctuations
        for punctuation in string.punctuation:
            if punctuation in splited_question:
                splited_question = splited_question.replace(punctuation, " ")

        splited_question = splited_question.split()

        # Remove keywords
        for keyword in self.keywords:
            for word in splited_question:
                if keyword in word:
                    splited_question.remove(word)

        parsed_question = []
        # Remove stopwords
        for word in splited_question:
            if word not in self.stopwords and len(word) > 1:
                parsed_question.append(word)

        self._parsed_input = " ".join(parsed_question)
