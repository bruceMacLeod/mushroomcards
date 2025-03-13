"""Service for flashcard operations."""
import logging
import os
from typing import Dict, List, Optional, Any

import pandas as pd

from config import Config
from models.flashcard import flashcard_state
from utils.csv_utils import load_csv_data
from utils.api_utils import get_taxon_id, get_observation_details

logger = logging.getLogger(__name__)


def check_answer(user_answer: str, card: Dict[str, Any]) -> Dict[str, Any]:
    """Check if the user's answer is correct."""
    user_answer = user_answer.strip().lower()
    
    if "scientific_name" not in card:
        return {"correct": False, "message": "Invalid card data received."}, 400
    
    if user_answer == card["scientific_name"].lower():
        common_name = card.get("common_name", "")
        return {"correct": True, "message": f"Correct! ({common_name})"}, 200
    
    return {"correct": False, "message": "Incorrect. Try again!"}, 200


def load_cards(filename: str, directory: str = "mmaforays") -> Dict[str, Any]:
    """Load all cards from a CSV file."""
    try:
        file_path = os.path.join(Config.BASE_DATA_DIR, directory, filename)
        if not os.path.exists(file_path):
            return {"error": "File not found"}, 404
        
        data = load_csv_data(file_path)
        if data is None:
            return {"error": "Failed to load CSV file"}, 500
        
        # Convert DataFrame to list of dictionaries
        cards = data.to_dict('records')
        return cards, 200
    
    except Exception as e:
        logger.error(f"Error in load_cards: {str(e)}")
        return {"error": str(e)}, 500


def select_csv_file(filename: str, directory: str = "mmaforays") -> Dict[str, Any]:
    """Select a CSV file for flashcards."""
    try:
        file_path = os.path.join(Config.BASE_DATA_DIR, directory, filename)
        if not os.path.exists(file_path):
            return {"error": "File not found"}, 404
        
        new_data = load_csv_data(file_path)
        if new_data is None:
            return {"error": "Failed to load CSV file"}, 500
        
        flashcard_state.update_current_file(file_path, directory, new_data)
        
        return {
            "message": "CSV file selected successfully",
            "first_card": new_data.iloc[0].to_dict(),
        }, 200
    
    except Exception as e:
        logger.error(f"Error in select_csv: {str(e)}")
        return {"error": str(e)}, 500


def process_csv_data(file_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process CSV data to add taxa_url and attribution if not present."""
    processed_rows = []
    
    for row in file_data:
        scientific_name = row.get("scientific_name", "")
        
        # Check if taxa_url already exists in the CSV
        taxa_url = row.get("taxa_url")
        if not taxa_url or taxa_url == "N/A":
            # Fetch the taxon_id and construct the taxa_url if not present
            taxon_id = get_taxon_id(scientific_name)
            taxa_url = f"https://www.inaturalist.org/taxa/{taxon_id}" if taxon_id else "N/A"
        
        # Check if attribution already exists
        attribution = row.get("attribution")
        if not attribution or attribution == "N/A":
            # Fetch observation details from iNaturalist API
            observation_url = row.get("url", "")
            if observation_url:
                observation_data = get_observation_details(observation_url)
                if observation_data and observation_data.get("photos"):
                    photo = observation_data["photos"][0]
                    attribution = photo.get('attribution', "N/A")
                else:
                    attribution = "N/A"
            else:
                attribution = "N/A"
        
        # Create a new row with only the required columns
        new_row = {
            "scientific_name": scientific_name,
            "common_name": row.get("common_name", "N/A"),
            "image_url": row.get("image_url", "N/A"),
            "taxa_url": taxa_url,
            "attribution": attribution
        }
        processed_rows.append(new_row)
    
    return processed_rows