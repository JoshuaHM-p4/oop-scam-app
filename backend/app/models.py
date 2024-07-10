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
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False) # represents ownership (many-to-one)
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

class UserFlashcardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    flashcard_set_id = db.Column(db.Integer, db.ForeignKey(FlashcardSet.id), nullable=False)

    def __repr__(self):
        return f'<UserFlashcardSet {self.user_id} - {self.flashcard_set_id}>'

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "flashcard_set_id": self.flashcard_set_id
        }

# Notebook, Note, UserNotebook, QuickNote, UserQuickNotes

class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.VARCHAR(64), nullable=False)

    def __repr__(self):
        return f'<Notebook {self.title}>'

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.owner_id,
            "title": self.title
        }

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notebook_id = db.Column(db.Integer, db.ForeignKey(Notebook.id), nullable=False)
    title = db.Column(db.VARCHAR(64), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Note {self.title}>'

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "note_id": self.note_id,
            "title": self.title,
            "content": self.content
        }
    
class UserNotebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    notebook_id = db.Column(db.Integer, db.ForeignKey(Notebook.id), nullable=False)

    def __repr__(self):
        return f'<UserNotebook {self.user_id} - {self.notebook_id}>'

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "notebook_id": self.notebook_id
        }

    
class QuickNote(db.Model):
    id = db.Column(db.Integer, primary_key=True) # quick note id
    title = db.Column(db.VARCHAR(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return f'<QuickNote {self.title}>'

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "owner_id": self.owner_id,
        }

class UserQuickNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    quick_note_id = db.Column(db.Integer, db.ForeignKey(QuickNote.id), nullable=False)

    def __repr__(self):
        return f'<UserQuickNotes {self.user_id} - {self.quick_note_id}>'
    
    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quick_note_id": self.quick_note_id
        }
    

###################################### Task ######################################

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)
    date = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), nullable=False) # Not-Started, In-Progress, Completed
    priority = db.Column(db.Integer, nullable=False) # High - 1, Medium - 2, Low - 3
    # added schema
    is_finished_at = db.Column(db.String(64), default=None)
    is_finished_by = db.Column(db.Integer, db.ForeignKey(User.id), default=None)

    def __repr__(self):
        return f'<Task {self.title}>'
    
    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "date": self.date,
            "type": self.type,
            "status": self.status,
            "priority": self.priority,
            "is_finished_by": self.is_finished_by,
            "is_finished_at": self.is_finished_at
        }
    
class UserTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __repr__(self):
        return f'<UserTask {self.user_id} - {self.task_id}>'
    
    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "task_id": self.task_id
        }


###################################### Team ######################################
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return f'<Team {self.name}>'
    
    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.team_name,
            "description": self.description,
            "owner_id": self.owner_id
        }
    
class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey(Team.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<TeamMember {self.team_id} - {self.user_id}>'
    
    def to_json(self) -> dict:
        return {
            "id": self.id,
            "team_id": self.team_id,
            "user_id": self.user_id
        }
    
class TeamTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey(Team.id), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id), nullable=False)

    def __repr__(self):
        return f'<TeamTask {self.team_id} - {self.task_id}>'
    
    def to_json(self) -> dict:
        return {
            "id": self.id,
            "team_id": self.team_id,
            "task_id": self.task_id
        }

def create_admin():
    # Check if the admin user already exists to avoid duplicates
    if not User.query.filter_by(username='admin').first():
        # Define admin user data
        admin_user = User(username='admin', email='admin')
        admin_user.set_password('1234')
        with db.session.begin_nested():
            db.session.add(admin_user)
        db.session.commit()
        print("Admin user added successfully.")

