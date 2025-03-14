"""Tests for models."""
import os
import pytest
import pandas as pd
import tempfile
import shutil
from unittest.mock import patch, mock_open
from models.pronunciation import PronunciationCache
from config import Config


from models.flashcard import FlashcardState
from models.pronunciation import PronunciationCache


class TestFlashcardState:
    """Test cases for FlashcardState model."""
    
    def test_initialization(self):
        """Test FlashcardState initialization."""
        state = FlashcardState()
        
        # Verify the initial state
        assert state.current_file["path"] is None
        assert state.current_file["directory"] is None
        assert state.current_file["data"] is None
    
    def test_update_current_file(self):
        """Test updating the current file."""
        state = FlashcardState()
        
        # Test data
        path = "/path/to/file.csv"
        directory = "uploads"
        data = pd.DataFrame({"scientific_name": ["Species 1", "Species 2"]})
        
        # Update the current file
        state.update_current_file(path, directory, data)
        
        # Verify the state was updated
        assert state.current_file["path"] == path
        assert state.current_file["directory"] == directory
        assert state.current_file["data"] is data  # Check reference equality
    
    def test_get_current_file(self):
        """Test getting the current file."""
        state = FlashcardState()
        
        # Test data
        path = "/path/to/file.csv"
        directory = "uploads"
        data = pd.DataFrame({"scientific_name": ["Species 1", "Species 2"]})
        
        # Update the current file
        state.update_current_file(path, directory, data)
        
        # Get the current file
        current_file = state.get_current_file()
        
        # Verify the result
        assert current_file["path"] == path
        assert current_file["directory"] == directory
        assert current_file["data"] is data  # Check reference equality




class TestPronunciationCache:
    """Test cases for PronunciationCache model."""

    @pytest.fixture
    def temp_cache_file(self):
        """Fixture to create a temporary cache file."""
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='') as temp_file:
            temp_file.write("scientific_name,pronunciation\nSpecies 1,Pronunciation 1\nSpecies 2,Pronunciation 2\n")
            temp_file_path = temp_file.name
        yield temp_file_path
        os.remove(temp_file_path)

    def test_load_cache(self, temp_cache_file):
        """Test loading cache from file."""
        # Override the cache file path with the temporary file
        Config.PRONUNCIATION_CACHE_FILE = temp_cache_file

        # Create a cache instance
        cache = PronunciationCache()

        # Verify the cache was loaded correctly
        assert len(cache.cache) == 2
        assert cache.cache["Species 1"] == "Pronunciation 1"
        assert cache.cache["Species 2"] == "Pronunciation 2"

    def test_initialize_cache_file_new(self):
        """Test initializing a new cache file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set the cache file path to a new file in the temporary directory
            temp_cache_file = os.path.join(temp_dir, "pronunciation_cache.csv")
            Config.PRONUNCIATION_CACHE_FILE = temp_cache_file

            # Create a cache instance
            cache = PronunciationCache()

            # Verify a new file was created
            assert os.path.exists(temp_cache_file)
            with open(temp_cache_file, 'r') as f:
                content = f.read()
                assert content == "scientific_name,pronunciation\n"

    def test_save_single_pronunciation(self, temp_cache_file):
        """Test saving a single pronunciation to the cache file."""
        # Override the cache file path with the temporary file
        Config.PRONUNCIATION_CACHE_FILE = temp_cache_file

        # Create a cache instance
        cache = PronunciationCache()

        # Save a single pronunciation
        result = cache.save_single_pronunciation("New Species", "New Pronunciation")

        # Verify the result
        assert result is True

        # Verify the file content
        with open(temp_cache_file, 'r') as f:
            lines = f.readlines()
            assert lines[-1] == "New Species,New Pronunciation\n"

    def test_save_all(self, temp_cache_file):
        """Test saving all pronunciations to the cache file."""
        # Override the cache file path with the temporary file
        Config.PRONUNCIATION_CACHE_FILE = temp_cache_file

        # Create a cache instance with test data
        cache = PronunciationCache()
        cache.cache = {"Species 1": "Pronunciation 1", "Species 2": "Pronunciation 2"}

        # Save all pronunciations
        cache.save_all()

        # Verify the file content
        with open(temp_cache_file, 'r') as f:
            content = f.read()
            assert content == (
                "scientific_name,pronunciation\n"
                "Species 1,Pronunciation 1\n"
                "Species 2,Pronunciation 2\n"
            )


