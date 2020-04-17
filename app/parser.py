import unicodedata


class Parser:
    def __init__(self, question):
        self.question = question

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

        self.question = sentences
