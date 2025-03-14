"""Model for pronunciation data."""
import csv
import fcntl
import logging
import os
from typing import Dict, Optional

from config import Config

logger = logging.getLogger(__name__)


class PronunciationCache:
    """Cache for scientific name pronunciations."""

    def __init__(self, cache_file_path="pronunciation_cache.csv"):
        self.cache_file_path = cache_file_path
        self.cache = self._load_cache()
#        self.cache = {}
        self._initialize_cache_file()



    def _load_cache(self) -> Dict[str, str]:
        """Load pronunciation cache from a CSV file."""
        cache = {}
        if os.path.exists(Config.PRONUNCIATION_CACHE_FILE):
            try:
                with open(Config.PRONUNCIATION_CACHE_FILE, "r") as f:
                    reader = csv.reader(f)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) == 2:
                            cache[row[0]] = row[1]
            except Exception as e:
                logger.error(f"Error loading pronunciation cache: {str(e)}")
        return cache
    
    def _initialize_cache_file(self) -> None:
        """Create the pronunciation cache file with headers if it doesn't exist 
        or appears to be corrupted."""
        create_new = False
        
        # Check if file exists
        if not os.path.exists(Config.PRONUNCIATION_CACHE_FILE):
            create_new = True
        else:
            # Check if file appears corrupted
            try:
                with open(Config.PRONUNCIATION_CACHE_FILE, "r") as f:
                    first_line = f.readline().strip()
                    if first_line != "scientific_name,pronunciation":
                        logger.warning("Pronunciation cache file appears corrupted, recreating")
                        create_new = True
            except Exception as e:
                logger.error(f"Error reading pronunciation cache file: {str(e)}")
                create_new = True
        
        # Create new file if needed
        if create_new:
            try:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(Config.PRONUNCIATION_CACHE_FILE), exist_ok=True)
                
                with open(Config.PRONUNCIATION_CACHE_FILE, "w", newline="") as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        writer = csv.writer(f)
                        writer.writerow(["scientific_name", "pronunciation"])
                        logger.info(f"Created new pronunciation cache file at {Config.PRONUNCIATION_CACHE_FILE}")
                    finally:
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except Exception as e:
                logger.error(f"Error initializing pronunciation cache file: {str(e)}")
    
    def get(self, name: str) -> Optional[str]:
        """Get pronunciation from cache."""
        return self.cache.get(name)
    
    def add(self, name: str, pronunciation: str) -> None:
        """Add pronunciation to cache."""
        self.cache[name] = pronunciation

    def save_single_pronunciation(self, scientific_name: str, pronunciation: str) -> bool:
        """
        Append a single pronunciation record to the cache file with file locking.
        Returns True if successful, False otherwise.
        """
        # Make sure the cache file exists
        if not os.path.exists(Config.PRONUNCIATION_CACHE_FILE):
            self._initialize_cache_file()

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(Config.PRONUNCIATION_CACHE_FILE), exist_ok=True)

            # Check if we can open the file
            with open(Config.PRONUNCIATION_CACHE_FILE, "r") as f:
                # Make sure the file has a header
                header = f.readline().strip()
                if header != "scientific_name,pronunciation":
                    logger.warning("Pronunciation cache file missing header, recreating")
                    self._initialize_cache_file()

            # Open file in append mode with file locking
            with open(Config.PRONUNCIATION_CACHE_FILE, "a", newline="") as f:
                # Acquire an exclusive lock
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    writer = csv.writer(f)
                    # Only write the new record
                    writer.writerow([scientific_name, pronunciation])
                    logger.info(f"Successfully saved pronunciation for {scientific_name} to cache file")
                    return True
                finally:
                    # Release the lock
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Exception as e:
            logger.error(f"Error saving pronunciation to cache: {str(e)}")
            return False

    def save_all(self) -> None:
        """Save all pronunciations to a CSV file."""
        try:
            with open(Config.PRONUNCIATION_CACHE_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["scientific_name", "pronunciation"])
                for name, pronunciation in self.cache.items():
                    writer.writerow([name, pronunciation])
        except Exception as e:
            logger.error(f"Error saving pronunciation cache: {str(e)}")


# Singleton instance
pronunciation_cache = PronunciationCache()