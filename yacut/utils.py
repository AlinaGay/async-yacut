import random
import re
import string
from flask import request
from urllib.parse import urlparse, parse_qs

from .models import URLMap

ALLOWED_CHARS = re.compile(r'^[A-Za-z0-9]{1,16}$')
RESERVED = {"files"}


def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    max_attempts = 10
    for attempt in range(max_attempts):
        short_id = ''.join(random.choice(characters) for _ in range(length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
    return generate_short_id(length + 1)


def validate_user_code(user_code):
    user_code = user_code.strip()
    if not ALLOWED_CHARS.fullmatch(user_code):
        raise ValueError("Только латинские буквы/цифры, длина ≤16")
    if (
        (user_code in RESERVED)
        or URLMap.query.filter_by(short=user_code).first()
    ):
        raise ValueError(
            "Предложенный вариант короткой ссылки уже существует.")
    return user_code


def generate_short_link(short_id):
    short_link = request.url_root + short_id
    return short_link


def is_yandex_disk_link(url):
    return any(domain in url for domain in [
        'yadi.sk', 'disk.yandex', 'yandex.ru/disk'])


def get_filename_from_url(url, fallback):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    filename = query_params.get("filename", [fallback])[0]
    return filename
