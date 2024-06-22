class FlashcardSetModel:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.flashcards = []

    def add_flashcard(self, flashcard):
        pass

class FlashcardModel:
    def __init__(self, id, set_id, word, definition):
        self.id = id
        self.set_id = set_id
        self.word = word
        self.definition = definition
