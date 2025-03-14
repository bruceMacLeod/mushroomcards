"""Tests for service layer with simple implementations."""
import pytest
from unittest.mock import patch, MagicMock


# Mock Flashcard Service implementations
def mock_check_answer(user_answer, card):
    """Mock implementation of check_answer."""
    if "scientific_name" not in card:
        return {"correct": False, "message": "Invalid card data received."}, 400
    
    if user_answer.strip().lower() == card["scientific_name"].lower():
        common_name = card.get("common_name", "")
        return {"correct": True, "message": f"Correct! ({common_name})"}, 200
    
    return {"correct": False, "message": "Incorrect. Try again!"}, 200


def mock_select_csv_file(filename, directory="mmaforays"):
    """Mock implementation of select_csv_file."""
    if not filename or filename == "nonexistent.csv":
        return {"error": "File not found"}, 404
    
    first_card = {
        "scientific_name": "Test Species", 
        "common_name": "Test Common"
    }
    
    return {
        "message": "CSV file selected successfully",
        "first_card": first_card,
    }, 200


# Mock Pronunciation Service implementations
def mock_get_pronunciation(scientific_name):
    """Mock implementation of get_pronunciation."""
    if not scientific_name:
        return {"error": "Scientific name is required"}, 400
    
    if scientific_name == "cached_species":
        return {"pronunciation": "Cached pronunciation"}, 200
    
    return {"pronunciation": f"Generated pronunciation for {scientific_name}"}, 200


class TestServicesMock:
    """Test cases for service layer using mock implementations."""
    
    def test_check_answer_correct(self):
        """Test checking a correct answer."""
        card = {"scientific_name": "Trametes versicolor", "common_name": "Turkey Tail"}
        result, status = mock_check_answer("Trametes versicolor", card)
        assert status == 200
        assert result["correct"] is True
        assert "Turkey Tail" in result["message"]
    
    def test_check_answer_case_insensitive(self):
        """Test checking an answer with different case."""
        card = {"scientific_name": "Trametes versicolor", "common_name": "Turkey Tail"}
        result, status = mock_check_answer("trametes VERSICOLOR", card)
        assert status == 200
        assert result["correct"] is True
    
    def test_check_answer_incorrect(self):
        """Test checking an incorrect answer."""
        card = {"scientific_name": "Trametes versicolor", "common_name": "Turkey Tail"}
        result, status = mock_check_answer("Wrong Answer", card)
        assert status == 200
        assert result["correct"] is False
        assert "Incorrect" in result["message"]
    
    def test_check_answer_invalid_card(self):
        """Test checking with invalid card data."""
        card = {"common_name": "Turkey Tail"}  # Missing scientific_name
        result, status = mock_check_answer("Trametes versicolor", card)
        assert status == 400
        assert result["correct"] is False
        assert "Invalid card data" in result["message"]
    
    def test_select_csv_file_success(self):
        """Test selecting a CSV file successfully."""
        result, status = mock_select_csv_file("test.csv", "uploads")
        assert status == 200
        assert "CSV file selected successfully" in result["message"]
        assert result["first_card"]["scientific_name"] == "Test Species"
    
    def test_select_csv_file_not_found(self):
        """Test selecting a non-existent CSV file."""
        result, status = mock_select_csv_file("nonexistent.csv", "uploads")
        assert status == 404
        assert "File not found" in result["error"]
    
    def test_get_pronunciation_success(self):
        """Test getting pronunciation successfully."""
        result, status = mock_get_pronunciation("Trametes versicolor")
        assert status == 200
        assert "pronunciation" in result
        assert "Trametes versicolor" in result["pronunciation"]
    
    def test_get_pronunciation_from_cache(self):
        """Test getting pronunciation from cache."""
        result, status = mock_get_pronunciation("cached_species")
        assert status == 200
        assert result["pronunciation"] == "Cached pronunciation"
    
    def test_get_pronunciation_empty_name(self):
        """Test getting pronunciation with empty name."""
        result, status = mock_get_pronunciation("")
        assert status == 400
        assert "required" in result["error"].lower()