"""Main application routes."""
import os
import logging
from flask import Blueprint, jsonify, render_template, send_from_directory

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def index():
    """Serve the main index page."""
    return render_template("index.html")


@main_bp.route("/wakeup", methods=["GET"])
def wakeup():
    """Simple endpoint to check if server is running."""
    return "Server is awake!", 200


@main_bp.route("/", defaults={"path": ""})
@main_bp.route("/<path:path>")
def serve(path: str):
    """Serve static files or fallback to index.html."""
    from flask import current_app
    
    if path and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    return send_from_directory(current_app.static_folder, "index.html")