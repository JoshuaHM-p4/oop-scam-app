from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.utils.error_handler import register_error_handlers

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app import models

    with app.app_context():
        db.create_all()
        db.session.commit()

        models.create_admin()

    register_error_handlers(app)

    from .routes.auth import auth_bp
    from .routes.notes import notes_bp
    # from .routes.templates import templates_bp
    # from .routes.calendar import calendar_bp
    # from .routes.progress import progress_bp
    from .routes.tasks import tasks_bp
    from .routes.flashcards import flashcards_bp
    from .routes.collaboration import collaboration_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    # app.register_blueprint(templates_bp)
    # app.register_blueprint(calendar_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(flashcards_bp)
    app.register_blueprint(collaboration_bp)

    return app
