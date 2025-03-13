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
    
    # Log the request
    logger.info(f"Fetching pronunciation for: {scientific_name}")
    
    # Check cache first
    cached_pronunciation = pronunciation_cache.get(scientific_name)
    if cached_pronunciation:
        logger.info(f"Found pronunciation for {scientific_name} in cache")
        return {"pronunciation": cached_pronunciation}, 200
    
    logger.info(f"No cached pronunciation found for {scientific_name}, generating new one")
    
    try:
        # Generate pronunciation using Gemini
        pronunciation = generate_pronunciation(scientific_name)
        if not pronunciation:
            logger.warning(f"Gemini model unavailable for {scientific_name}, using fallback")
            # Fallback when Gemini is unavailable
            fallback = f"Pronunciation for {scientific_name} is unavailable. Please try again later."
            return {"pronunciation": fallback, "warning": "Using fallback pronunciation"}, 200
        
        logger.info(f"Successfully generated pronunciation for {scientific_name}")
        
        # Update in-memory cache
        pronunciation_cache.add(scientific_name, pronunciation)
        logger.info(f"Added pronunciation for {scientific_name} to in-memory cache")
        
        # Try to save to file
        cache_result = pronunciation_cache.save_single_pronunciation(scientific_name, pronunciation)
        if cache_result:
            logger.info(f"Successfully saved pronunciation for {scientific_name} to cache file")
            return {"pronunciation": pronunciation}, 200
        else:
            # If save failed, still return the pronunciation but log the error
            logger.warning(f"Failed to save pronunciation for {scientific_name} to cache file")
            return {
                "pronunciation": pronunciation,
                "warning": "Pronunciation generated but not cached to file"
            }, 200
    
    except Exception as e:
        logger.error(f"Error in get_pronunciation for {scientific_name}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "error": f"Error generating pronunciation: {str(e)}",
            "scientific_name": scientific_name
        }, 500