class FlashcardSetModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.flashcards = []

    def add_flashcard(self, flashcard):
        self.flashcards.append(flashcard)

    @classmethod
    def from_json(cls, data: dict) -> 'FlashcardSetModel':
        return cls(
        id = data["id"],
        name = data["name"]
        )

class FlashcardModel:
    def __init__(self, id, set_id, word, definition):
        self.id = id
        self.set_id = set_id
        self.word = word
        self.definition = definition
