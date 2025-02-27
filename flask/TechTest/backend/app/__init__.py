from flask import Flask

from config import settings
from app.db.session import db
from app.db.models.Book import Book
from app.db.models.Loan import Loan
from app.db.models.User import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    # Initialize Flask extensions here
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.books import bp as books_bp
    app.register_blueprint(books_bp, url_prefix="/book")

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix="/user")

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app