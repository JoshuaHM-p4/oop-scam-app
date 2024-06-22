from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth import auth_bp
    from .routes.notes import notes_bp
    from .routes.templates import templates_bp
    from .routes.calendar import calendar_bp
    from .routes.tasks import tasks_bp
    from .routes.flashcards import flashcards_bp
    from .routes.collaboration import collaboration_bp

    # app.register_blueprint(auth_bp)
    # app.register_blueprint(notes_bp)
    # app.register_blueprint(templates_bp)
    # app.register_blueprint(calendar_bp)
    # app.register_blueprint(tasks_bp)
    # app.register_blueprint(flashcards_bp)
    # app.register_blueprint(collaboration_bp)

    return app
