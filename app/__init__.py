from flask import Flask
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Load configurations
    db.init_app(app)  # Initialize SQLAlchemy

    # Import and register blueprints
    from app.views.student import student
    app.register_blueprint(student, url_prefix='/students')

    return app
