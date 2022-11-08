from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os 

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if test_config:
        app.config["TESTING"]=True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
        app.config['TEST_SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'TEST_SQLALCHEMY_DATABASE_URI'
            )
    else:   
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False 
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'SQLALCHEMY_DATABASE_URI'
            ) 

    db.init_app(app)
    migrate.init_app(app, db)
    
    #import models here

    from app.models.book import Book
    from app.models.author import Author

    db.init_app(app)
    migrate.init_app(app, db)

    #register blueprints here
    from .book_routes import books_bp
    app.register_blueprint(books_bp)

    from .author_routes import authors_bp
    app.register_blueprint(authors_bp)
    return app

 