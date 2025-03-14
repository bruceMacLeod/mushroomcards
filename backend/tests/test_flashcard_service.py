"""Tests for flashcard service."""
import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from models.flashcard import FlashcardState
from services.flashcard_service import check_answer, load_cards, select_csv_file, process_csv_data


class TestFlashcardService:
    """Test cases for flashcard service functions."""
    
    def test_check_answer_correct(self):
        """Test checking a correct answer."""
        # Test data
        card = {"scientific_name": "Trametes versicolor", "common_name": "Turkey Tail"}
        user_answer = "Trametes versicolor"
        
        # Test the function
        result, status = check_answer(user_answer, card)
        
        # Verify the result
        assert result["correct"] is True
        assert "Turkey Tail" in result["message"]
        assert status == 200
    
    def test_check_answer_correct_case_insensitive(self):
        """Test checking a correct answer with different case."""
        # Test data
        card = {"scientific_name": "Trametes versicolor", "common_name": "Turkey Tail"}
        user_answer = "trametes VERSICOLOR"
        
        # Test the function
        result, status = check_answer(user_answer, card)
        
        # Verify the result
        assert result["correct"] is True
        assert status == 200
    
    def test_check_answer_incorrect(self):
        """Test checking an incorrect answer."""
        # Test data
        card = {"scientific_name": "Trametes versicolor", "common_name": "Turkey Tail"}
        user_answer = "Pleurotus ostreatus"
        
        # Test the function
        result, status = check_answer(user_answer, card)
        
        # Verify the result
        assert result["correct"] is False
        assert "Incorrect" in result["message"]
        assert status == 200
    
    def test_check_answer_invalid_card(self):
        """Test checking an answer with invalid card data."""
        # Test data
        card = {"common_name": "Turkey Tail"}  # Missing scientific_name
        user_answer = "Trametes versicolor"
        
        # Test the function
        result, status = check_answer(user_answer, card)
        
        # Verify the result
        assert result["correct"] is False
        assert "Invalid card data" in result["message"]
        assert status == 400
    
    @patch('services.flashcard_service.load_csv_data')
    def test_load_cards_success(self, mock_load_csv):
        """Test loading cards successfully."""
        # Mock the CSV loading
        mock_data = pd.DataFrame({
            "scientific_name": ["Species 1", "Species 2"],
            "common_name": ["Common 1", "Common 2"],
            "image_url": ["https://example.com/1.jpg", "https://example.com/2.jpg"],
            "attribution": ["Attribution 1", "Attribution 2"],
            "taxa_url": ["https://example.com/taxa/1", "https://example.com/taxa/2"]
        })
        mock_load_csv.return_value = mock_data
        
        # Mock the file existence check
        with patch('os.path.exists', return_value=True):
            # Test the function
            result, status = load_cards("test.csv", "uploads")
            
            # Verify the result
            assert status == 200
            assert len(result) == 2
            assert result[0]["scientific_name"] == "Species 1"
            assert result[1]["common_name"] == "Common 2"
    
    @patch('services.flashcard_service.load_csv_data')
    def test_load_cards_file_not_found(self, mock_load_csv):
        """Test loading cards with file not found."""
        # Mock the file existence check
        with patch('os.path.exists', return_value=False):
            # Test the function
            result, status = load_cards("nonexistent.csv", "uploads")
            
            # Verify the result
            assert status == 404
            assert "File not found" in result["error"]
    
    @patch('services.flashcard_service.load_csv_data')
    def test_load_cards_csv_load_failure(self, mock_load_csv):
        """Test loading cards with CSV loading failure."""
        # Mock the CSV loading to return None (failure)
        mock_load_csv.return_value = None
        
        # Mock the file existence check
        with patch('os.path.exists', return_value=True):
            # Test the function
            result, status = load_cards("test.csv", "uploads")
            
            # Verify the result
            assert status == 500
            assert "Failed to load CSV file" in result["error"]
    
    @patch('services.flashcard_service.load_csv_data')
    def test_select_csv_file_success(self, mock_load_csv):
        """Test selecting a CSV file successfully."""
        # Mock the CSV loading
        mock_data = pd.DataFrame({
            "scientific_name": ["Species 1", "Species 2"],
            "common_name": ["Common 1", "Common 2"],
            "image_url": ["https://example.com/1.jpg", "https://example.com/2.jpg"],
            "attribution": ["Attribution 1", "Attribution 2"],
            "taxa_url": ["https://example.com/taxa/1", "https://example.com/taxa/2"]
        })
        mock_load_csv.return_value = mock_data
        
        # Mock the file existence check
        with patch('os.path.exists', return_value=True):
            # Test the function
            result, status = select_csv_file("test.csv", "uploads")
            
            # Verify the result
            assert status == 200
            assert "CSV file selected successfully" in result["message"]
            assert result["first_card"]["scientific_name"] == "Species 1"
    
    def test_process_csv_data_complete_data(self):
        """Test processing CSV data with complete information."""
        # Test data with all fields present
        file_data = [
            {
                "scientific_name": "Trametes versicolor",
                "common_name": "Turkey Tail",
                "image_url": "https://example.com/image.jpg",
                "attribution": "Photo by Test User",
                "taxa_url": "https://example.com/taxa/12345"
            }
        ]
        
        # Test the function
        result = process_csv_data(file_data)
        
        # Verify the result
        assert len(result) == 1
        assert result[0]["scientific_name"] == "Trametes versicolor"
        assert result[0]["common_name"] == "Turkey Tail"
        assert result[0]["image_url"] == "https://example.com/image.jpg"
        assert result[0]["attribution"] == "Photo by Test User"
        assert result[0]["taxa_url"] == "https://example.com/taxa/12345"
    
    @patch('services.flashcard_service.get_taxon_id')
    def test_process_csv_data_missing_taxa_url(self, mock_get_taxon_id):
        """Test processing CSV data with missing taxa_url."""
        # Mock the taxon_id retrieval
        mock_get_taxon_id.return_value = 12345
        
        # Test data with missing taxa_url
        file_data = [
            {
                "scientific_name": "Trametes versicolor",
                "common_name": "Turkey Tail",
                "image_url": "https://example.com/image.jpg",
                "attribution": "Photo by Test User"
            }
        ]
        
        # Test the function
        result = process_csv_data(file_data)
        
        # Verify the result
        assert len(result) == 1
        assert result[0]["scientific_name"] == "Trametes versicolor"
        assert result[0]["taxa_url"] == "https://www.inaturalist.org/taxa/12345"
    
    @patch('services.flashcard_service.get_taxon_id')
    @patch('services.flashcard_service.get_observation_details')
    def test_process_csv_data_missing_attribution(self, mock_get_obs, mock_get_taxon_id):
        """Test processing CSV data with missing attribution."""
        # Mock the observation details retrieval
        mock_get_obs.return_value = {
            "photos": [
                {"attribution": "Photo by iNaturalist User"}
            ]
        }
        
        # Test data with missing attribution
        file_data = [
            {
                "scientific_name": "Trametes versicolor",
                "common_name": "Turkey Tail",
                "image_url": "https://example.com/image.jpg",
                "taxa_url": "https://example.com/taxa/12345",
                "url": "https://www.inaturalist.org/observations/12345"
            }
        ]
        
        # Test the function
        result = process_csv_data(file_data)
        
        # Verify the result
        assert len(result) == 1
        assert result[0]["scientific_name"] == "Trametes versicolor"
        assert result[0]["attribution"] == "Photo by iNaturalist User"
    
    def test_process_csv_data_missing_scientific_name(self):
        """Test processing CSV data with missing scientific_name."""
        # Test data with missing scientific_name
        file_data = [
            {
                "common_name": "Turkey Tail",
                "image_url": "https://example.com/image.jpg",
                "attribution": "Photo by Test User",
                "taxa_url": "https://example.com/taxa/12345"
            }
        ]
        
        # Test the function
        result = process_csv_data(file_data)
        
        # Verify the result
        assert len(result) == 0  # Row should be skipped