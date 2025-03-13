"""Utilities for CSV file operations."""
import csv
import logging
import os
import traceback
from typing import Dict, List, Optional, Any

import pandas as pd

from config import Config

logger = logging.getLogger(__name__)


def load_csv_data(file_path: str) -> Optional[pd.DataFrame]:
    """Load CSV data and return DataFrame.
    
    Args:
        file_path: Absolute path to the CSV file to load
        
    Returns:
        DataFrame containing the CSV data or None if loading failed
    """
    if not os.path.exists(file_path):
        logger.error(f"CSV file not found: {file_path}")
        return None
        
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check for required columns
        required_columns = ["image_url", "scientific_name", "common_name", "taxa_url", "attribution"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"CSV file {file_path} missing required columns: {', '.join(missing_columns)}")
            return None
            
        # Filter to required columns and remove rows with missing values
        data = df[required_columns].dropna()
        logger.info(f"Successfully loaded {len(data)} rows from {file_path}")
        return data
        
    except pd.errors.EmptyDataError:
        logger.error(f"CSV file {file_path} is empty")
        return None
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing CSV file {file_path}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error loading CSV from {file_path}: {str(e)}")
        logger.error(traceback.format_exc())
        return None


def list_csv_files(directory: str = "mmaforays") -> List[str]:
    """List CSV files in a directory in alphabetical order.
    
    Args:
        directory: Directory name to list files from (default: "mmaforays")
        
    Returns:
        List of CSV filenames sorted alphabetically
    """
    # Determine directory path based on directory name
    if directory == "mmaforays":
        directory_path = Config.SPECIES_DATA_DIR
    else:
        directory_path = Config.UPLOADS_DIR
    
    # Check if directory exists
    if not os.path.exists(directory_path):
        logger.error(f"Directory not found: {directory_path}")
        return []
    
    # Get CSV files and sort them alphabetically
    try:
        csv_files = sorted([f for f in os.listdir(directory_path) if f.endswith(".csv")], key=str.lower)
        logger.info(f"Found {len(csv_files)} CSV files in {directory}")
        return csv_files
    except PermissionError:
        logger.error(f"Permission denied accessing directory: {directory_path}")
        return []
    except Exception as e:
        logger.error(f"Error listing CSV files in {directory_path}: {str(e)}")
        logger.error(traceback.format_exc())
        return []


def save_csv_data(file_path: str, rows: List[Dict[str, Any]], fieldnames: List[str]) -> bool:
    """Save data to a CSV file.
    
    Args:
        file_path: Absolute path where the CSV file should be saved
        rows: List of dictionaries containing the data
        fieldnames: List of column names to include
        
    Returns:
        True if save was successful, False otherwise
    """
    # Ensure directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {str(e)}")
            return False
    
    try:
        # Write the CSV file
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        logger.info(f"Successfully saved {len(rows)} rows to {file_path}")
        return True
    except PermissionError:
        logger.error(f"Permission denied writing to file: {file_path}")
        return False
    except Exception as e:
        logger.error(f"Error saving CSV data to {file_path}: {str(e)}")
        logger.error(traceback.format_exc())
        return False