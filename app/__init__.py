from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from .config import Config

mongo = PyMongo()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Update CORS configuration
    # CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
    CORS(app, origins=["*"])
    # Initialize MongoDB and SocketIO
    mongo.init_app(app)
    socketio.init_app(app, cors_allowed_origins="http://localhost:5173")

    with app.app_context():
        from . import routes  # Import routes
        return app
