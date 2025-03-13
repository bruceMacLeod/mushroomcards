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
    
    def __init__(self):
        """Initialize pronunciation cache."""
        self.cache = self._load_cache()
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
        """Create the pronunciation cache file with headers if it doesn't exist."""
        if not os.path.exists(Config.PRONUNCIATION_CACHE_FILE):
            try:
                with open(Config.PRONUNCIATION_CACHE_FILE, "w", newline="") as f:
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                    try:
                        writer = csv.writer(f)
                        writer.writerow(["scientific_name", "pronunciation"])
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
        try:
            # Open file in append mode with file locking
            with open(Config.PRONUNCIATION_CACHE_FILE, "a", newline="") as f:
                # Acquire an exclusive lock
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    writer = csv.writer(f)
                    # Only write the new record
                    writer.writerow([scientific_name, pronunciation])
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