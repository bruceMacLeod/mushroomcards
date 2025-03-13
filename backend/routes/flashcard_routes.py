"""Routes for flashcard operations."""
import csv
import logging
import os
import traceback
from typing import Dict, List, Any, Tuple, Optional

from flask import Blueprint, jsonify, request, Response
from werkzeug.utils import secure_filename

from config import Config
from models.flashcard import flashcard_state
from services.flashcard_service import check_answer, load_cards, select_csv_file, process_csv_data
from utils.csv_utils import list_csv_files, save_csv_data

# Configure module logger
logger = logging.getLogger(__name__)

# Create blueprint for flashcard routes
flashcard_bp = Blueprint('flashcard', __name__)


@flashcard_bp.route("/check_answer", methods=["POST"])
def check_answer_route() -> Tuple[Response, int]:
    """Check if the user's answer is correct.
    
    Expects JSON with:
    - "answer": the user's provided answer
    - "card": dictionary containing "scientific_name" and optionally "common_name"
    
    Returns:
        JSON response with correct/incorrect status and HTTP status code
    """
    try:
        # Validate request has JSON data
        if not request.is_json:
            logger.warning("Request to check_answer missing JSON")
            return jsonify({"error": "Missing JSON in request"}), 400
            
        payload = request.json
        user_answer = payload.get("answer", "")
        card = payload.get("card", {})
        
        if not user_answer:
            logger.warning("Empty answer provided to check_answer")
            return jsonify({"error": "Answer is required"}), 400
            
        if not card:
            logger.warning("Empty card provided to check_answer")
            return jsonify({"error": "Card data is required"}), 400
        
        # Process the answer check
        logger.debug(f"Checking answer: '{user_answer}' against card")
        result, status_code = check_answer(user_answer, card)
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in check_answer route: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@flashcard_bp.route("/load_cards", methods=["POST"])
def load_cards_route():
    """Load all cards from a CSV file."""
    payload = request.json
    filename = payload.get("filename")
    directory = payload.get("directory", "mmaforays")
    
    result, status_code = load_cards(filename, directory)
    return jsonify(result), status_code


@flashcard_bp.route("/list_csv_files", methods=["GET"])
def list_csv_files_route():
    """List CSV files in a directory in alphabetical order."""
    directory = request.args.get("directory", "mmaforays")
    csv_files = list_csv_files(directory)
    return jsonify({"files": csv_files}), 200


@flashcard_bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    """Upload a CSV file, add a taxa_url column if not present, and save specific columns."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    directory = request.form.get("directory", "uploads")
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith(".csv"):
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.BASE_DATA_DIR, directory, filename)
            
            # Read the uploaded CSV file directly from the request
            file_stream = file.stream.read().decode("utf-8").splitlines()
            reader = csv.DictReader(file_stream)
            rows = list(reader)
            
            # Process the data to add taxa_url and attribution if needed
            processed_rows = process_csv_data(rows)
            
            # Save the processed data to a CSV file
            fieldnames = ["scientific_name", "common_name", "image_url", "taxa_url", "attribution"]
            if save_csv_data(file_path, processed_rows, fieldnames):
                return jsonify({
                    "message": "File uploaded and modified successfully",
                    "filename": filename
                }), 200
            else:
                return jsonify({"error": "Failed to save CSV file"}), 500
        
        except Exception as e:
            logger.error(f"Error in upload_csv: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file type"}), 400


@flashcard_bp.route("/upload_csv_json", methods=["POST"])
def upload_csv_json():
    """
    Upload a CSV file, process it to add taxa_url and attribution if needed,
    and return the processed records as JSON without saving the file.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith(".csv"):
        try:
            # Read the uploaded CSV file
            file_stream = file.stream.read().decode("utf-8").splitlines()
            reader = csv.DictReader(file_stream)
            rows = list(reader)
            
            # Process the data
            processed_rows = process_csv_data(rows)
            
            # Return the processed records as JSON
            return jsonify({
                "message": "File processed successfully",
                "records": processed_rows
            }), 200
        
        except Exception as e:
            logger.error(f"Error processing CSV file: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file type"}), 400


@flashcard_bp.route("/select_csv", methods=["POST"])
def select_csv():
    """Select a CSV file for flashcards."""
    payload = request.json
    filename = payload.get("filename")
    directory = payload.get("directory", "mmaforays")
    
    result, status_code = select_csv_file(filename, directory)
    return jsonify(result), status_code


@flashcard_bp.route("/delete_csv/<filename>", methods=["DELETE"])
def delete_csv(filename: str) -> Tuple[Response, int]:
    """Delete a CSV file.
    
    Args:
        filename: The name of the file to delete

    Query Parameters:
        directory: The directory containing the file (default: "uploads")
        
    Returns:
        JSON response with success/error message and HTTP status code
    """
    # Validate file extension
    if not filename.endswith(".csv"):
        logger.warning(f"Attempt to delete non-CSV file: {filename}")
        return jsonify({"error": "Invalid file type - only CSV files can be deleted"}), 400
    
    # Get directory from query parameters
    directory = request.args.get("directory", "uploads")
    
    # Security check - verify filename doesn't contain path traversal
    if ".." in filename or "/" in filename:
        logger.warning(f"Potential path traversal attempt in filename: {filename}")
        return jsonify({"error": "Invalid filename"}), 400
    
    # Construct full file path
    file_path = os.path.join(Config.BASE_DATA_DIR, directory, filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        logger.warning(f"File not found for deletion: {file_path}")
        return jsonify({"error": "File not found"}), 404
    
    try:
        # Delete the file
        os.remove(file_path)
        logger.info(f"Successfully deleted file: {file_path}")
        return jsonify({"message": "File deleted successfully"}), 200
    except PermissionError:
        logger.error(f"Permission denied deleting file: {file_path}")
        return jsonify({"error": "Permission denied - cannot delete file"}), 403
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Failed to delete file: {str(e)}"}), 500