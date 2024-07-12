class FlashcardSetModel:
    def __init__(self, id, user_id, name):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.starred = False
        self.flashcards = []

    def add_flashcard(self, flashcard):
        self.flashcards.append(flashcard)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{self.id} - {self.name} - {'starred' if self.starred else ''} - {len(self.flashcards)} Flashcards"

class FlashcardModel:
    def __init__(self, id, set_id, word, definition):
        self.id = id
        self.set_id = set_id
        self.word = word
        self.definition = definition
