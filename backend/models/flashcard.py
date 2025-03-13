"""Model for flashcard data."""
from typing import Dict, Any, Optional


class FlashcardState:
    """Global state management for flashcard data."""
    
    def __init__(self) -> None:
        """Initialize flashcard state with empty current file data."""
        self.current_file: Dict[str, Any] = {
            "path": None,
            "directory": None,
            "data": None,
        }
    
    def update_current_file(self, path: str, directory: str, data: Any) -> None:
        """Update the current file information.
        
        Args:
            path: The file path of the current file
            directory: The directory name containing the file
            data: The loaded data from the file
        """
        self.current_file["path"] = path
        self.current_file["directory"] = directory 
        self.current_file["data"] = data
    
    def get_current_file(self) -> Dict[str, Any]:
        """Get the current file information.
        
        Returns:
            Dictionary containing path, directory and data
        """
        return self.current_file


# Singleton instance
flashcard_state = FlashcardState()