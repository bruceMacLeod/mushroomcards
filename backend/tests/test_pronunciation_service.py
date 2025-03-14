"""Tests for pronunciation service."""
import pytest
from unittest.mock import patch, MagicMock

from models.pronunciation import pronunciation_cache
from services.pronunciation_service import get_pronunciation


class TestPronunciationService:
    """Test cases for pronunciation service functions."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Reset the cache for each test
        pronunciation_cache.cache = {}
    
    @patch('services.pronunciation_service.pronunciation_cache.get')
    def test_get_pronunciation_from_cache(self, mock_cache_get):
        """Test getting pronunciation from cache."""
        # Mock the cache to return a value
        mock_cache_get.return_value = "The pronunciation of Trametes versicolor is tra-MEE-teez ver-si-COLOR."
        
        # Test the function
        result, status = get_pronunciation("Trametes versicolor")
        
        # Verify the result
        assert status == 200
        assert result["pronunciation"] == "The pronunciation of Trametes versicolor is tra-MEE-teez ver-si-COLOR."
        # Verify the cache call
        mock_cache_get.assert_called_once_with("Trametes versicolor")
    
    @patch('services.pronunciation_service.pronunciation_cache.get')
    @patch('services.pronunciation_service.generate_pronunciation')
    @patch('services.pronunciation_service.pronunciation_cache.add')
    @patch('services.pronunciation_service.pronunciation_cache.save_single_pronunciation')
    def test_get_pronunciation_generate_new(self, mock_save, mock_add, mock_generate, mock_cache_get):
        """Test generating new pronunciation when not in cache."""
        # Mock the cache to return None (cache miss)
        mock_cache_get.return_value = None
        
        # Mock generating a new pronunciation
        mock_generate.return_value = "The pronunciation of Trametes versicolor is tra-MEE-teez ver-si-COLOR."
        
        # Mock the successful cache save
        mock_save.return_value = True
        
        # Test the function
        result, status = get_pronunciation("Trametes versicolor")
        
        # Verify the result
        assert status == 200
        assert result["pronunciation"] == "The pronunciation of Trametes versicolor is tra-MEE-teez ver-si-COLOR."
        
        # Verify the function calls
        mock_cache_get.assert_called_once()
        mock_generate.assert_called_once()
        mock_add.assert_called_once()
        mock_save.assert_called_once()
    
    @patch('services.pronunciation_service.pronunciation_cache.get')
    @patch('services.pronunciation_service.generate_pronunciation')
    @patch('services.pronunciation_service.pronunciation_cache.add')
    @patch('services.pronunciation_service.pronunciation_cache.save_single_pronunciation')
    def test_get_pronunciation_save_failure(self, mock_save, mock_add, mock_generate, mock_cache_get):
        """Test getting pronunciation but failing to save to cache file."""
        # Mock the cache to return None (cache miss)
        mock_cache_get.return_value = None
        
        # Mock generating a new pronunciation
        mock_generate.return_value = "The pronunciation of Trametes versicolor is tra-MEE-teez ver-si-COLOR."
        
        # Mock the cache save to fail
        mock_save.return_value = False
        
        # Test the function
        result, status = get_pronunciation("Trametes versicolor")
        
        # Verify the result
        assert status == 200
        assert result["pronunciation"] == "The pronunciation of Trametes versicolor is tra-MEE-teez ver-si-COLOR."
        assert "warning" in result
        
        # Verify the function calls
        mock_cache_get.assert_called_once()
        mock_generate.assert_called_once()
        mock_add.assert_called_once()
        mock_save.assert_called_once()
    
    @patch('services.pronunciation_service.pronunciation_cache.get')
    @patch('services.pronunciation_service.generate_pronunciation')
    def test_get_pronunciation_generation_failure(self, mock_generate, mock_cache_get):
        """Test getting pronunciation with generation failure."""
        # Mock the cache to return None (cache miss)
        mock_cache_get.return_value = None

        # Mock generating a new pronunciation to fail
        mock_generate.return_value = None

        # Test the function
        result, status = get_pronunciation("Trametes versicolor")

        # Verify the result
        assert status == 200
        assert "unavailable" in result["pronunciation"].lower()  # Check for "unavailable" instead of "fallback"
        assert "warning" in result


    def test_get_pronunciation_empty_name(self):
        """Test getting pronunciation with empty name."""
        # Test the function with empty string
        result, status = get_pronunciation("")
        
        # Verify the result
        assert status == 400
        assert "required" in result["error"].lower()
    
    @patch('services.pronunciation_service.pronunciation_cache.get')
    @patch('services.pronunciation_service.generate_pronunciation')
    def test_get_pronunciation_unexpected_error(self, mock_generate, mock_cache_get):
        """Test getting pronunciation with an unexpected error."""
        # Mock the cache to return None (cache miss)
        mock_cache_get.return_value = None
        
        # Mock generating a new pronunciation to raise an exception
        mock_generate.side_effect = Exception("Unexpected error")
        
        # Test the function
        result, status = get_pronunciation("Trametes versicolor")
        
        # Verify the result
        assert status == 500
        assert "error" in result
        assert result["scientific_name"] == "Trametes versicolor"