"""Main application entry point."""
import logging
import os

# Try to import dotenv, but continue if it fails
try:
    from dotenv import load_dotenv
    # Load environment variables
    load_dotenv()
except ImportError:
    logging.warning("python-dotenv not installed, skipping environment variable loading")
    
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from models.flashcard import flashcard_state
from models.pronunciation import pronunciation_cache
from routes.flashcard_routes import flashcard_bp
from routes.main_routes import main_bp
from routes.pronunciation_routes import pronunciation_bp
from utils.csv_utils import load_csv_data

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Environment variables are loaded in the try/except block above


def create_app(test_config=None):
    """Create and configure the Flask app."""
    # Initialize Flask app
    app = Flask(__name__)
    
    # Initialize directories
    Config.init_directories()
    
    # Configure CORS
    CORS(
        app,
        resources={
            r"/*": {
                "origins": os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
            }
        }
    )
    
    # Load initial data
    initialize_app_data()
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(flashcard_bp)
    app.register_blueprint(pronunciation_bp)
    
    # Add global error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle all exceptions."""
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500
    
    return app


def initialize_app_data():
    """Initialize application data."""
    # Load initial flashcard data
    if os.path.exists(Config.INITIAL_FILE_PATH):
        initial_data = load_csv_data(Config.INITIAL_FILE_PATH)
        flashcard_state.update_current_file(
            Config.INITIAL_FILE_PATH,
            "uploads",
            initial_data
        )
    else:
        logger.warning(f"Initial file not found: {Config.INITIAL_FILE_PATH}")


# Create the app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)