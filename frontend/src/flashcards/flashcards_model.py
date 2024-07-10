class FlashcardSetModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.starred = False
        self.flashcards = []

    def add_flashcard(self, flashcard):
        self.flashcards.append(flashcard)

class FlashcardModel:
    def __init__(self, id, set_id, word, definition):
        self.id = id
        self.set_id = set_id
        self.word = word
        self.definition = definition
