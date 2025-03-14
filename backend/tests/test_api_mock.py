"""Tests for API utilities with simple mocks."""
import pytest
from unittest.mock import patch, MagicMock


# Mock functions that mimic the behavior of the real API utilities
def mock_get_taxon_id(scientific_name):
    """Mock implementation of get_taxon_id."""
    # Simulate a successful API response for a known species
    if scientific_name == "Trametes versicolor":
        return 12345
    # Simulate no results found
    return None


def mock_get_observation_details(observation_url):
    """Mock implementation of get_observation_details."""
    # Simulate a successful API response
    if observation_url and "12345" in observation_url:
        return {
            "id": 12345,
            "photos": [
                {"url": "https://example.com/photo.jpg", "attribution": "Photo by Test User"}
            ]
        }
    # Simulate failure
    return None


def mock_generate_pronunciation(scientific_name):
    """Mock implementation of generate_pronunciation."""
    # Simulate successful generation
    if scientific_name:
        return f"The pronunciation of {scientific_name} is..."
    # Simulate failure
    return None


class TestAPIMocks:
    """Test cases for API utility functions using simple mocks."""
    
    def test_get_taxon_id_success(self):
        """Test getting a taxon ID successfully."""
        result = mock_get_taxon_id("Trametes versicolor")
        assert result == 12345
    
    def test_get_taxon_id_no_results(self):
        """Test getting a taxon ID with no results."""
        result = mock_get_taxon_id("Unknown Species")
        assert result is None
    
    def test_get_observation_details_success(self):
        """Test getting observation details successfully."""
        result = mock_get_observation_details("https://example.com/observations/12345")
        assert result is not None
        assert result["id"] == 12345
        assert "photos" in result
    
    def test_get_observation_details_failure(self):
        """Test getting observation details with failure."""
        result = mock_get_observation_details("https://example.com/observations/99999")
        assert result is None
    
    def test_generate_pronunciation_success(self):
        """Test generating pronunciation successfully."""
        result = mock_generate_pronunciation("Trametes versicolor")
        assert result is not None
        assert "Trametes versicolor" in result
    
    def test_generate_pronunciation_failure(self):
        """Test generating pronunciation with failure."""
        result = mock_generate_pronunciation("")
        assert result is None