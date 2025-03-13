# Mushroom Cards - Style Guide

This document defines the coding style standards for the Mushroom Cards application.

## Python (Backend)

### Naming Conventions

- Use `snake_case` for variables, functions, methods, and modules
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants
- Prefix private methods and variables with a single underscore (`_`)

### Function Definitions

- Always include type hints for parameters and return values
- When a function doesn't return anything, explicitly use `-> None`
- Use explicit return type annotations for all functions
- Order parameters with required parameters first, then optional parameters with defaults

Example:
```python
def process_data(input_data: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
    """Process the input data and return a list of processed items."""
    # Function implementation
    return processed_items
```

### Error Handling

- Use specific exception types when possible
- Always include error messages with context in exception handling
- Log errors with appropriate logging levels
- Return consistent error responses from API endpoints:
  - `{"error": "Error message"}` with appropriate status code
- Use try/except blocks around operations that might fail

Example:
```python
try:
    data = load_csv_data(file_path)
    if data is None:
        return {"error": "Failed to load CSV file"}, 500
    # Process data
except Exception as e:
    logger.error(f"Error processing file {file_path}: {str(e)}")
    return {"error": f"Error processing file: {str(e)}"}, 500
```

### Import Style

- Group imports in the following order, with a blank line between each group:
  1. Standard library imports
  2. Third-party library imports 
  3. Local application imports
- Sort imports alphabetically within each group
- Use absolute imports for application modules

Example:
```python
import csv
import logging
import os
from typing import Dict, List, Optional

import pandas as pd
from flask import Blueprint, jsonify, request

from config import Config
from models.pronunciation import pronunciation_cache
from utils.csv_utils import load_csv_data
```

### Documentation

- Every module, class, and function should have a docstring
- Use triple double-quotes for docstrings (`"""Docstring"""`)
- Keep single-line docstrings on one line
- For multi-line docstrings, put the closing quotes on a new line
- Include parameter descriptions for complex functions

Example:
```python
def generate_pronunciation(scientific_name: str) -> Optional[str]:
    """Generate pronunciation using Gemini AI.
    
    Args:
        scientific_name: The scientific name to generate pronunciation for
        
    Returns:
        The pronunciation as a string, or None if generation failed
    """
    # Function implementation
```

### Comments

- Use comments sparingly - prefer clear code and good function/variable names
- Always put a space after the `#`
- Comments should explain "why", not "what"
- Don't leave commented-out code in the codebase

## JavaScript (Frontend)

- Use camelCase for variables, functions, and methods
- Use PascalCase for React components and class names
- Prefer arrow functions for callbacks and component methods
- Use explicit destructuring for props
- Consistent error handling using try/catch or error state management