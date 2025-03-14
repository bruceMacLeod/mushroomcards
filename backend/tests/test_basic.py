"""Basic tests to verify the testing setup."""
import pytest


def test_app_exists(app):
    """Test that the app fixture works."""
    assert app is not None


def test_app_config(app):
    """Test that the app is configured for testing."""
    assert app.config['TESTING'] is True


def test_client_works(client):
    """Test that the client fixture works."""
    response = client.get('/')
    assert response is not None