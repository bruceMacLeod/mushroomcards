"""Service for flashcard operations."""
import logging
import os
import traceback
from typing import Dict, List, Optional, Any, Tuple

import pandas as pd

from config import Config
from models.flashcard import flashcard_state
from utils.csv_utils import load_csv_data
from utils.api_utils import get_taxon_id, get_observation_details

logger = logging.getLogger(__name__)


def check_answer(user_answer: str, card: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """Check if the user's answer is correct.
    
    Args:
        user_answer: The answer provided by the user
        card: The flashcard data containing the scientific name
        
    Returns:
        A tuple containing response data and HTTP status code
    """
    user_answer = user_answer.strip().lower()
    
    if "scientific_name" not in card:
        logger.warning("Invalid card data received - missing scientific_name")
        return {"correct": False, "message": "Invalid card data received."}, 400
    
    if user_answer == card["scientific_name"].lower():
        common_name = card.get("common_name", "")
        return {"correct": True, "message": f"Correct! ({common_name})"}, 200
    
    return {"correct": False, "message": "Incorrect. Try again!"}, 200


def load_cards(filename: str, directory: str = "mmaforays") -> Tuple[Dict[str, Any], int]:
    """Load all cards from a CSV file.
    
    Args:
        filename: Name of the CSV file to load
        directory: Directory containing the file (default: "mmaforays")
        
    Returns:
        A tuple containing either the cards data or error info, and HTTP status code
    """
    try:
        file_path = os.path.join(Config.BASE_DATA_DIR, directory, filename)
        
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return {"error": "File not found"}, 404
        
        data = load_csv_data(file_path)
        if data is None:
            logger.error(f"Failed to load CSV file: {file_path}")
            return {"error": "Failed to load CSV file"}, 500
        
        # Convert DataFrame to list of dictionaries
        cards = data.to_dict('records')
        logger.info(f"Successfully loaded {len(cards)} cards from {filename}")
        return cards, 200
    
    except Exception as e:
        logger.error(f"Error in load_cards for {filename}: {str(e)}")
        logger.error(traceback.format_exc())
        return {"error": f"Error loading cards: {str(e)}"}, 500


def select_csv_file(filename: str, directory: str = "mmaforays") -> Tuple[Dict[str, Any], int]:
    """Select a CSV file for flashcards and update current file state.
    
    Args:
        filename: Name of the CSV file to select
        directory: Directory containing the file (default: "mmaforays")
        
    Returns:
        A tuple containing response data and HTTP status code
    """
    try:
        file_path = os.path.join(Config.BASE_DATA_DIR, directory, filename)
        
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            return {"error": "File not found"}, 404
        
        new_data = load_csv_data(file_path)
        if new_data is None:
            logger.error(f"Failed to load CSV file: {file_path}")
            return {"error": "Failed to load CSV file"}, 500
        
        flashcard_state.update_current_file(file_path, directory, new_data)
        logger.info(f"Successfully selected CSV file: {filename}")
        
        return {
            "message": "CSV file selected successfully",
            "first_card": new_data.iloc[0].to_dict(),
        }, 200
    
    except Exception as e:
        logger.error(f"Error in select_csv_file for {filename}: {str(e)}")
        logger.error(traceback.format_exc())
        return {"error": f"Error selecting CSV file: {str(e)}"}, 500


def process_csv_data(file_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process CSV data to add taxa_url and attribution if not present.
    
    Args:
        file_data: List of dictionaries containing row data from CSV
        
    Returns:
        List of processed row dictionaries with complete data
    """
    processed_rows = []
    
    try:
        for row in file_data:
            scientific_name = row.get("scientific_name", "")
            if not scientific_name:
                logger.warning("Row missing scientific_name, skipping")
                continue
                
            # Process taxa_url
            taxa_url = row.get("taxa_url")
            if not taxa_url or taxa_url == "N/A":
                try:
                    # Fetch the taxon_id and construct the taxa_url if not present
                    taxon_id = get_taxon_id(scientific_name)
                    taxa_url = f"https://www.inaturalist.org/taxa/{taxon_id}" if taxon_id else "N/A"
                except Exception as e:
                    logger.error(f"Error fetching taxon_id for {scientific_name}: {str(e)}")
                    taxa_url = "N/A"
            
            # Process attribution
            attribution = row.get("attribution")
            if not attribution or attribution == "N/A":
                try:
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
                except Exception as e:
                    logger.error(f"Error fetching attribution for {scientific_name}: {str(e)}")
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
        
        logger.info(f"Successfully processed {len(processed_rows)} rows")
        return processed_rows
        
    except Exception as e:
        logger.error(f"Error in process_csv_data: {str(e)}")
        logger.error(traceback.format_exc())
        # Return what we have so far, rather than failing completely
        return processed_rows