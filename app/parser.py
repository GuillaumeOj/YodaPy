import unicodedata


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
        key_words = [
            'ou est',
            'trouve',
            'adresse',
            'lieu',
            'situe',
            'alle',
            'direction',
            'endroit',
            'rue',
            'boulevard',
            'avenue',
            'impasse',
            'route',
            'chemin',
            'village',
            'ville',
            'port',
            'jete',
            'viaduc',
            'pont',
        ]

        self.split_sentences()

        user_question = ''

        for key_word in key_words:
            for sentence in self.question:
                if key_word in sentence:
                    user_question = sentence

        self.question = user_question
