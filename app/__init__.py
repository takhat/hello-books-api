from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    
    from app.routes import book_bp
    app.register_blueprint(book_bp)
    
    return app