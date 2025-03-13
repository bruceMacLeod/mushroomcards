"""Model for flashcard data."""
from typing import Dict, Any, Optional


class FlashcardState:
    """Global state management for flashcard data."""
    
    def __init__(self):
        """Initialize flashcard state."""
        self.current_file = {
            "path": None,
            "directory": None,
            "data": None,
        }
    
    def update_current_file(self, path: str, directory: str, data: Any) -> None:
        """Update the current file information."""
        self.current_file["path"] = path
        self.current_file["directory"] = directory 
        self.current_file["data"] = data
    
    def get_current_file(self) -> Dict[str, Any]:
        """Get the current file information."""
        return self.current_file


# Singleton instance
flashcard_state = FlashcardState()