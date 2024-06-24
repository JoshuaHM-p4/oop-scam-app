from app import create_app

import sqlalchemy as sa
from app.models import User, Flashcard, FlashcardSet
from app import db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'db': db, 'User': User, 'FlashcardSet': FlashcardSet, 'Flashcard': Flashcard}

if __name__ == "__main__":
    app.run()