"""Routes for pronunciation operations."""
import logging
from flask import Blueprint, jsonify, request

from services.pronunciation_service import get_pronunciation

logger = logging.getLogger(__name__)

pronunciation_bp = Blueprint('pronunciation', __name__)


@pronunciation_bp.route("/pronounce_name", methods=["POST"])
def pronounce_name():
    """Get pronunciation for a scientific name."""
    payload = request.json
    scientific_name = payload.get("scientific_name", "")
    
    result, status_code = get_pronunciation(scientific_name)
    return jsonify(result), status_code