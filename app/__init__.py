from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from .config import Config
from flask_jwt_extended import JWTManager

mongo = PyMongo()
jwt = JWTManager() 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Enable CORS for all routes
    mongo.init_app(app)  # Initialize PyMongo with the app
    jwt.init_app(app)  
    with app.app_context():
        from . import routes  # Import routes
        return app