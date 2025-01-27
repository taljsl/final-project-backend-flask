from dotenv import load_dotenv  # Import load_dotenv
from app import create_app
import os

load_dotenv()  # Load environment variables from .env file

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production