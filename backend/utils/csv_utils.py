"""Utilities for CSV file operations."""
import csv
import logging
import os
from typing import Dict, List, Optional

import pandas as pd

from config import Config

logger = logging.getLogger(__name__)


def load_csv_data(file_path: str) -> Optional[pd.DataFrame]:
    """Load CSV data and return DataFrame."""
    try:
        required_columns = ["image_url", "scientific_name", "common_name", "taxa_url", "attribution"]
        data = pd.read_csv(file_path)[required_columns].dropna()
        return data
    except Exception as e:
        logger.error(f"Error loading CSV: {str(e)}")
        return None


def list_csv_files(directory: str = "mmaforays") -> List[str]:
    """List CSV files in a directory in alphabetical order."""
    if directory == "mmaforays":
        directory_path = Config.SPECIES_DATA_DIR
    else:
        directory_path = Config.UPLOADS_DIR
    
    # Get CSV files and sort them alphabetically
    try:
        csv_files = sorted([f for f in os.listdir(directory_path) if f.endswith(".csv")], key=str.lower)
        return csv_files
    except Exception as e:
        logger.error(f"Error listing CSV files: {str(e)}")
        return []


def save_csv_data(file_path: str, rows: List[Dict], fieldnames: List[str]) -> bool:
    """Save data to a CSV file."""
    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return True
    except Exception as e:
        logger.error(f"Error saving CSV data: {str(e)}")
        return False