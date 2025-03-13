"""Routes for pronunciation operations."""
import logging
import os
from flask import Blueprint, jsonify, request

from config import Config
from models.pronunciation import pronunciation_cache
from services.pronunciation_service import get_pronunciation
from utils.api_utils import generate_pronunciation

logger = logging.getLogger(__name__)

pronunciation_bp = Blueprint('pronunciation', __name__)


@pronunciation_bp.route("/pronounce_name", methods=["POST"])
def pronounce_name():
    """Get pronunciation for a scientific name."""
    payload = request.json
    scientific_name = payload.get("scientific_name", "")
    
    # Log pronunciation request for debugging
    logger.info(f"Pronunciation requested for: {scientific_name}")
    
    result, status_code = get_pronunciation(scientific_name)
    return jsonify(result), status_code


@pronunciation_bp.route("/debug_pronunciation", methods=["GET"])
def debug_pronunciation():
    """Debug endpoint for pronunciation service."""
    # Check if pronunciation cache file exists
    cache_file_exists = os.path.exists(Config.PRONUNCIATION_CACHE_FILE)
    
    # Check file permissions
    file_permissions = "Unknown"
    if cache_file_exists:
        try:
            file_permissions = oct(os.stat(Config.PRONUNCIATION_CACHE_FILE).st_mode)[-3:]
        except Exception as e:
            file_permissions = f"Error checking permissions: {str(e)}"
    
    # Check if we can write to the file
    can_write = False
    try:
        if not cache_file_exists:
            # Create the file if it doesn't exist
            with open(Config.PRONUNCIATION_CACHE_FILE, "w") as f:
                f.write("scientific_name,pronunciation\n")
            can_write = True
        else:
            # Try to append to the file
            with open(Config.PRONUNCIATION_CACHE_FILE, "a") as f:
                f.write("") 
            can_write = True
    except Exception as e:
        logger.error(f"Error writing to cache file: {str(e)}")
    
    # Test adding a test pronunciation to the cache
    test_name = "Test_Species"
    test_pronunciation = "This is a test pronunciation"
    
    cache_result = None
    try:
        # Add to in-memory cache
        pronunciation_cache.add(test_name, test_pronunciation)
        # Try to save to file
        save_result = pronunciation_cache.save_single_pronunciation(test_name, test_pronunciation)
        cache_result = f"Save result: {save_result}"
    except Exception as e:
        cache_result = f"Error saving to cache: {str(e)}"
    
    # Test Gemini model
    gemini_result = None
    try:
        test_gemini = generate_pronunciation("Amanita muscaria")
        gemini_result = "Gemini model working" if test_gemini else "Gemini model not available"
    except Exception as e:
        gemini_result = f"Error with Gemini: {str(e)}"
    
    # Return debug info
    return jsonify({
        "pronunciation_cache_file": Config.PRONUNCIATION_CACHE_FILE,
        "file_exists": cache_file_exists,
        "file_permissions": file_permissions,
        "can_write": can_write,
        "cache_test": cache_result,
        "gemini_test": gemini_result,
        "cache_size": len(pronunciation_cache.cache)
    }), 200