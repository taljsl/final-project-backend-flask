from dotenv import load_dotenv  # Import load_dotenv
from app import create_app, socketio
import os

load_dotenv()  # Load environment variables from .env file

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)  # Use socketio.run instead of app.run