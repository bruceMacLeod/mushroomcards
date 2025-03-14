"""Test fixtures and configuration for pytest."""
import os
import sys
import pytest
from flask import Flask

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create a simple mock app for testing
# This avoids dependency issues when importing the real app

def create_test_app(test_config=None):
    app = Flask(__name__,
                template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')))
#    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'BASE_DATA_DIR': os.path.join(os.path.dirname(__file__), 'test_data'),
    })
    
    if test_config:
        app.config.update(test_config)
    
    # Create necessary test directories
    os.makedirs(os.path.join(app.config['BASE_DATA_DIR'], 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.config['BASE_DATA_DIR'], 'mmaforays'), exist_ok=True)
    # Register routes or blueprints here
    from routes.main_routes import main_bp
    from routes.flashcard_routes import flashcard_bp
    from routes.pronunciation_routes import pronunciation_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(flashcard_bp)
    app.register_blueprint(pronunciation_bp)

    return app


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create the test app
    app = create_test_app()
    
    # Return the app for testing
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()