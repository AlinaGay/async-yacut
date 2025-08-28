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

from . import app, db
from .error_handlers import APIUsageError
from .models import URLMap
from .utils import (
    ALLOWED_CHARS, RESERVED,
    generate_short_link,
    get_unique_short_id
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Handle POST requests for creating a new short link."""
    data = request.get_json(silent=True) or {}
    if not data:
        raise APIUsageError('Отсутствует тело запроса', 400)

    original_url = (data.get('url') or '').strip()
    if not original_url:
        raise APIUsageError('"url" является обязательным полем!', 400)

    short_code = data.get('custom_id')
    if (short_code in RESERVED) or (not ALLOWED_CHARS.fullmatch(short_code)):
        raise APIUsageError(
            'Указано недопустимое имя для короткой ссылки', 400)
    if URLMap.query.filter_by(short=short_code).first():
        raise APIUsageError(
            'Предложенный вариант короткой ссылки уже существует.', 400)
    if not short_code:
        short_code = get_unique_short_id()

    db.session.add(URLMap(original=original_url, short=short_code))
    db.session.commit()
    short_link = generate_short_link(short_code)
    return jsonify({"url": original_url, "short_link": short_link}), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Handle GET requests for resolving a short ID to its original URL."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise APIUsageError('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
