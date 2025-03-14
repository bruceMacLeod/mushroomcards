"""Integration tests for API routes."""
import json
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from models.flashcard import flashcard_state
from models.pronunciation import pronunciation_cache


class TestMainRoutes:
    """Test cases for main routes."""
    
    def test_index(self, client):
        """Test the main route."""
        response = client.get('/')
        assert response.status_code == 200
        assert response.data
    
    def test_list_csv_files(self, client):
        """Test listing CSV files."""
        with patch('routes.main_routes.list_csv_files') as mock_list:
            # Mock the list_csv_files function to return sample files
            mock_list.return_value = ["file1.csv", "file2.csv"]
            
            # Test the route
            response = client.get('/list_csv_files?directory=uploads')
            
            # Verify the response
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "files" in data
            assert data["files"] == ["file1.csv", "file2.csv"]


class TestFlashcardRoutes:
    """Test cases for flashcard routes."""
    
    def setup_method(self):
        """Set up test data before each test."""
        # Reset flashcard state
        flashcard_state.current_file = {
            "path": None,
            "directory": None,
            "data": None,
        }
    
    @patch('services.flashcard_service.load_cards')
    def test_get_all_cards(self, mock_load_cards, client):
        """Test getting all cards."""
        # Mock the load_cards function
        mock_cards = [
            {"scientific_name": "Species 1", "common_name": "Common 1"},
            {"scientific_name": "Species 2", "common_name": "Common 2"}
        ]
        mock_load_cards.return_value = (mock_cards, 200)
        
        # Test the route
        response = client.get('/cards/test.csv?directory=uploads')
        
        # Verify the response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]["scientific_name"] == "Species 1"
    
    @patch('services.flashcard_service.check_answer')
    def test_check_answer(self, mock_check_answer, client):
        """Test checking an answer."""
        # Mock the check_answer function
        mock_result = {"correct": True, "message": "Correct!"}
        mock_check_answer.return_value = (mock_result, 200)
        
        # Test data
        test_data = {
            "answer": "Trametes versicolor",
            "card": {"scientific_name": "Trametes versicolor", "common_name": "Turkey Tail"}
        }
        
        # Test the route
        response = client.post('/check_answer', 
                              data=json.dumps(test_data),
                              content_type='application/json')
        
        # Verify the response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["correct"] is True
    
    @patch('services.flashcard_service.select_csv_file')
    def test_select_flashcard_file(self, mock_select, client):
        """Test selecting a flashcard file."""
        # Mock the select_csv_file function
        mock_result = {
            "message": "CSV file selected successfully",
            "first_card": {"scientific_name": "Species 1", "common_name": "Common 1"}
        }
        mock_select.return_value = (mock_result, 200)
        
        # Test the route
        response = client.post('/select_file', 
                              data=json.dumps({"filename": "test.csv", "directory": "uploads"}),
                              content_type='application/json')
        
        # Verify the response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "message" in data
        assert data["first_card"]["scientific_name"] == "Species 1"


class TestPronunciationRoutes:
    """Test cases for pronunciation routes."""
    
    def setup_method(self):
        """Set up test data before each test."""
        # Reset pronunciation cache
        pronunciation_cache.cache = {}
    
    @patch('services.pronunciation_service.get_pronunciation')
    def test_get_pronunciation(self, mock_get_pronunciation, client):
        """Test getting a pronunciation."""
        # Mock the get_pronunciation function
        mock_result = {"pronunciation": "The pronunciation is..."}
        mock_get_pronunciation.return_value = (mock_result, 200)
        
        # Test the route
        response = client.get('/pronunciation/Trametes%20versicolor')
        
        # Verify the response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "pronunciation" in data
    
    @patch('services.pronunciation_service.get_pronunciation')
    def test_get_pronunciation_error(self, mock_get_pronunciation, client):
        """Test getting a pronunciation with an error."""
        # Mock the get_pronunciation function to return an error
        mock_result = {"error": "Scientific name is required"}
        mock_get_pronunciation.return_value = (mock_result, 400)
        
        # Test the route with an empty name
        response = client.get('/pronunciation/')
        
        # Verify the response
        assert response.status_code == 404  # Flask returns 404 for routes without parameters