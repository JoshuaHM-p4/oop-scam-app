from app import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
class FlashcardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)

    def __repr__(self):
        return f'<Card {self.name}>'

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name
        }

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flashcard_set_id = db.Column(db.Integer, db.ForeignKey(FlashcardSet.id), nullable=False)
    word = db.Column(db.Text, nullable=False)
    definition = db.Column(db.Text, nullable=False)

    def __rep__(self):
        return f'{self.word} - {self.definition}'

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "flashcard_set_id": self.flashcard_set_id,
            "word": self.word,
            "definition": self.definition
        }
