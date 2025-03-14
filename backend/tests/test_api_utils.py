"""Tests for API utilities."""
import pytest
from unittest.mock import patch, MagicMock

from utils.api_utils import get_taxon_id, get_observation_details, generate_pronunciation


class TestAPIUtils:
    """Test cases for API utility functions."""
    
    @patch('utils.api_utils.requests.get')
    def test_get_taxon_id_success(self, mock_get):
        """Test getting a taxon ID successfully."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"id": 12345, "name": "Trametes versicolor"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Test the function
        result = get_taxon_id("Trametes versicolor")
        
        # Verify the result
        assert result == 12345
        # Verify the API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == "https://api.inaturalist.org/v1/taxa"
        assert kwargs["params"]["q"] == "Trametes versicolor"
    
    @patch('utils.api_utils.requests.get')
    def test_get_taxon_id_no_results(self, mock_get):
        """Test getting a taxon ID with no results."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response
        
        # Test the function
        result = get_taxon_id("Unknown Species")
        
        # Verify the result
        assert result is None
    
    @patch('utils.api_utils.requests.get')
    def test_get_taxon_id_api_error(self, mock_get):
        """Test getting a taxon ID with API error."""
        # Mock the API response to raise an exception
        mock_get.side_effect = Exception("API Error")
        
        # Test the function
        result = get_taxon_id("Trametes versicolor")
        
        # Verify the result
        assert result is None
    
    @patch('utils.api_utils.requests.get')
    def test_get_observation_details_success(self, mock_get):
        """Test getting observation details successfully."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": 12345,
                    "photos": [
                        {"url": "https://example.com/photo.jpg", "attribution": "Photo by Test User"}
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test the function
        result = get_observation_details("https://www.inaturalist.org/observations/12345")
        
        # Verify the result
        assert result is not None
        assert result["id"] == 12345
        assert result["photos"][0]["url"] == "https://example.com/photo.jpg"
        # Verify the API call
        mock_get.assert_called_once_with("https://api.inaturalist.org/v1/observations/12345")
    
    @patch('utils.api_utils.requests.get')
    def test_get_observation_details_api_error(self, mock_get):
        """Test getting observation details with API error."""
        # Mock the API response to raise an exception
        mock_get.side_effect = Exception("API Error")
        
        # Test the function
        result = get_observation_details("https://www.inaturalist.org/observations/12345")
        
        # Verify the result
        assert result is None
    
    @patch('utils.api_utils.model')
    def test_generate_pronunciation_success(self, mock_model):
        """Test generating pronunciation successfully."""
        # Mock the Gemini model response
        mock_response = MagicMock()
        mock_response.text = "The pronunciation of Trametes versicolor is tra-MEE-teez ver-si-COLOR."
        mock_model.generate_content.return_value = mock_response
        
        # Test the function
        result = generate_pronunciation("Trametes versicolor")
        
        # Verify the result
        assert result == "The pronunciation of Trametes versicolor is tra-MEE-teez ver-si-COLOR."
        # Verify the API call
        mock_model.generate_content.assert_called_once()
        args, kwargs = mock_model.generate_content.call_args
        assert args[0] == "Pronounce Trametes versicolor using English Scientific Latin with explanation"
    
    @patch('utils.api_utils.model')
    def test_generate_pronunciation_model_error(self, mock_model):
        """Test generating pronunciation with model error."""
        # Mock the Gemini model to raise an exception
        mock_model.generate_content.side_effect = Exception("Model Error")
        
        # Test the function
        result = generate_pronunciation("Trametes versicolor")
        
        # Verify the result
        assert result is None
    
    def test_generate_pronunciation_no_model(self):
        """Test generating pronunciation with no model available."""
        # Temporarily set model to None for the test
        with patch('utils.api_utils.model', None):
            # Test the function
            result = generate_pronunciation("Trametes versicolor")
            
            # Verify the result
            assert result is None