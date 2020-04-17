class Parser:
    def __init__(self, user_input):
        self.user_input = user_input
        self.question = ''

    def lower_text(self):
        self.question = self.user_input.lower()
