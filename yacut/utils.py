"""Utility functions for the YaCut URL-shortening service.

This module provides helpers for:
- Generating unique short identifiers (`get_unique_short_id`).
- Validating user-provided short codes (`validate_user_code`).
- Building absolute short links (`generate_short_link`).
- Detecting Yandex Disk URLs (`is_yandex_disk_link`).
- Extracting filenames from download URLs (`get_filename_from_url`).

It also defines:
- `ALLOWED_CHARS`: Regex pattern for valid short codes
(A–Z, a–z, 0–9, up to 16 chars).
- `RESERVED`: A set of reserved short codes that cannot be used by users.
"""

import random
import re
import string
from flask import request
from urllib.parse import urlparse, parse_qs

from .models import URLMap

ALLOWED_CHARS = re.compile(r'^[A-Za-z0-9]{1,16}$')
RESERVED = {"files"}


def get_unique_short_id(length=6):
    """Generate a unique short identifier not present in the database."""
    characters = string.ascii_letters + string.digits
    max_attempts = 10
    for attempt in range(max_attempts):
        short_id = ''.join(random.choice(characters) for _ in range(length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
    return get_unique_short_id(length + 1)


def validate_user_code(user_code):
    """Validate a user-provided custom short code."""
    user_code = user_code.strip()
    if not ALLOWED_CHARS.fullmatch(user_code):
        raise ValueError('Только латинские буквы/цифры, длина ≤16')
    if (
        (user_code in RESERVED) or
        URLMap.query.filter_by(short=user_code).first()
    ):
        raise ValueError(
            'Предложенный вариант короткой ссылки уже существует.')
    return user_code


def generate_short_link(short_id):
    """Build a fully qualified short link for a given short ID."""
    short_link = request.url_root + short_id
    return short_link


def is_yandex_disk_link(url):
    """Check whether a URL points to Yandex Disk."""
    return any(domain in url for domain in [
        'yadi.sk', 'disk.yandex', 'yandex.ru/disk'])


def get_filename_from_url(url, fallback):
    """Extract the filename from a Yandex Disk (or similar) URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filename = query_params.get("filename", [fallback])[0]
    return filename
