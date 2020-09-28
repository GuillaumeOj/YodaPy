"""Parse the user input"""
import unicodedata
import os.path
import json


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


class Parser:
    """Parse a user input"""

    def __init__(self):
        self.parsed_input = ""

        # Load stopwords from a json file
        stopwords_path = os.path.join(CURRENT_DIR, "static/json/stopwords.json")
        self.stopwords = []
        with open(stopwords_path) as json_f:
            self.stopwords = json.load(json_f)

        # Load keywords for the question from a json file
        keywords_path = os.path.join(CURRENT_DIR, "static/json/keywords.json")
        self.keywords = []
        with open(keywords_path) as json_f:
            self.keywords = json.load(json_f)

    def parse(self, user_input):
        """Launch each method for parsing the user input"""
        self.parsed_input = user_input

        self.normalize()
        self.split_sentences()
        self.find_question()
        self.clear_question()

        if self.parsed_input:
            self.parsed_input = {"parsed_input": self.parsed_input}

        return self.parsed_input

    def normalize(self):
        """Lower and replace accents"""
        self.parsed_input = self.parsed_input.lower()

        unicode_text = unicodedata.normalize("NFD", self.parsed_input)
        ascii_unaccented = unicode_text.encode("ascii", "ignore")
        self.parsed_input = ascii_unaccented.decode("utf8")

    def split_sentences(self):
        """Split the input in a list of sentences"""
        sentences = []
        start = 0
        for i, character in enumerate(self.parsed_input):
            if character in "?.!,":
                sentences.append(self.parsed_input[start:i].strip())
                start = i + 1
        if sentences:
            self.parsed_input = sentences
        else:
            self.parsed_input = [self.parsed_input]

    def find_question(self):
        """Find the question in a list of sentences"""
        question = []
        for keyword in self.keywords:
            for sentence in self.parsed_input:
                if keyword in sentence:
                    question.append(sentence)

        # Keep only the last question
        if question:
            self.parsed_input = question[-1]
        else:
            self.parsed_input = ""

    def clear_question(self):
        """Remove useless words (stopwords and keywords)"""
        # Remove quotes
        removed_quotes = self.parsed_input.replace("'", " ")
        removed_hyphens = removed_quotes.replace("-", " ")
        splited_question = removed_hyphens.split()

        # Remove keywords
        parsed_question = [
            word for word in splited_question if word not in self.keywords
        ]

        # Remove stopwords
        parsed_question = [
            word
            for word in parsed_question
            if word not in self.stopwords and len(word) > 1
        ]

        self.parsed_input = " ".join(parsed_question)
