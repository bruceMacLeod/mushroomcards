"""Service for pronunciation operations."""
import logging
from typing import Dict, Optional

from models.pronunciation import pronunciation_cache
from utils.api_utils import generate_pronunciation

logger = logging.getLogger(__name__)


def get_pronunciation(scientific_name: str) -> Dict[str, str]:
    """Get pronunciation for a scientific name."""
    if not scientific_name:
        return {"error": "Scientific name is required"}, 400
    
    # Check cache first
    cached_pronunciation = pronunciation_cache.get(scientific_name)
    if cached_pronunciation:
        return {"pronunciation": cached_pronunciation}, 200
    
    try:
        # Generate pronunciation using Gemini
        pronunciation = generate_pronunciation(scientific_name)
        if not pronunciation:
            logger.warning("Gemini model unavailable, using fallback pronunciation")
            # Fallback when Gemini is unavailable
            fallback = f"Pronunciation for {scientific_name} is unavailable. Please try again later."
            return {"pronunciation": fallback, "warning": "Using fallback pronunciation"}, 200
        
        # Update cache
        pronunciation_cache.add(scientific_name, pronunciation)
        
        # Try to save to file
        if pronunciation_cache.save_single_pronunciation(scientific_name, pronunciation):
            return {"pronunciation": pronunciation}, 200
        else:
            # If save failed, still return the pronunciation but log the error
            logger.warning("Failed to save pronunciation to cache file")
            return {
                "pronunciation": pronunciation,
                "warning": "Pronunciation generated but not cached"
            }, 200
    
    except Exception as e:
        logger.error(f"Error in get_pronunciation: {str(e)}")
        return {"error": str(e)}, 500