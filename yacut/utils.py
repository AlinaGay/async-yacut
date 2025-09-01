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

import re
from flask import request
from urllib.parse import urlparse, parse_qs


ALLOWED_CHARS = re.compile(r'^[A-Za-z0-9]{1,16}$')
RESERVED = {"files"}


def generate_short_link(short_id):
    """Build a fully qualified short link for a given short ID."""
    short_link = request.url_root + short_id
    return short_link


def get_filename_from_url(url, fallback):
    """Extract the filename from a Yandex Disk (or similar) URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filename = query_params.get("filename", [fallback])[0]
    return filename
