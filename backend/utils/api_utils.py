"""Utilities for API interactions."""
import logging
import os
from typing import Optional, Dict, Any

import requests

logger = logging.getLogger(__name__)

# Try to import google.generativeai, but continue if it fails
try:
    import google.generativeai as genai
    # Configure Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
    else:
        logger.warning("GEMINI_API_KEY not found in environment variables")
        model = None
except ImportError:
    logger.warning("google-generativeai package not installed, AI features disabled")
    model = None


def get_taxon_id(scientific_name: str) -> Optional[int]:
    """Fetch the taxon_id for a given scientific name from iNaturalist."""
    url = "https://api.inaturalist.org/v1/taxa"
    params = {"q": scientific_name, "rank": "species"}
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0].get("id")
        
        logger.info(f"No taxon_id found for {scientific_name}.")
        return None
    except Exception as e:
        logger.error(f"Error fetching taxon_id: {str(e)}")
        return None


def get_observation_details(observation_url: str) -> Optional[Dict[str, Any]]:
    """Fetch observation details from iNaturalist API."""
    if not observation_url:
        return None
    
    try:
        observation_id = observation_url.split("/")[-1]
        observation_response = requests.get(
            f"https://api.inaturalist.org/v1/observations/{observation_id}")
        
        if observation_response.status_code == 200:
            return observation_response.json().get("results", [{}])[0]
        
        return None
    except Exception as e:
        logger.error(f"Error fetching observation details: {str(e)}")
        return None


def generate_pronunciation(scientific_name: str) -> Optional[str]:
    """Generate pronunciation using Gemini AI."""
    if not model:
        logger.error("Gemini model not initialized")
        return None
    
    try:
        prompt = f"Pronounce {scientific_name} using English Scientific Latin with explanation"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating pronunciation: {str(e)}")
        return None