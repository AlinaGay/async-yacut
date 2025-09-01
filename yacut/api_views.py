"""API views for the YaCut URL-shortening service.

This module defines the REST API endpoints for working with shortened links:

- POST `/api/id/`:
    Create a new short link for a given original URL, optionally using a
    user-provided custom ID. Returns the original URL and the generated
    short link.

- GET `/api/id/<short_id>/`:
    Retrieve the original URL associated with the provided short ID.

The endpoints follow the specification described in the project requirements
(openapi.yml).
"""

from flask import jsonify, request

from . import app
from .error_handlers import APIUsageError
from .models import URLMap
from .utils import generate_short_link


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Handle POST requests for creating a new short link."""
    data = request.get_json(silent=True) or {}
    if not data:
        raise APIUsageError('Отсутствует тело запроса', 400)
    try:
        obj = URLMap.validate_user_code(
            original_url=data.get('url'),
            custom_id=data.get('custom_id'),
        )
    except ValueError as e:
        raise APIUsageError(str(e), 400)
    return jsonify({
        "url": obj.original,
        "short_link": generate_short_link(obj.short)
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Handle GET requests for resolving a short ID to its original URL."""
    url_map = URLMap.get_by_short(short_id)
    if not url_map:
        raise APIUsageError('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
