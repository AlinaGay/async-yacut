import random
import re
import string
from flask import request

from .models import URLMap

ALLOWED_CHARS = re.compile(r'^[A-Za-z0-9]{1,16}$')
RESERVED = {"files"}


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    max_attempts = 10
    for attempt in range(max_attempts):
        short_code = ''.join(random.choice(characters) for _ in range(length))
        if not URLMap.query.filter_by(short=short_code).first():
            return short_code
    return generate_short_code(length + 1)


def validate_user_code(user_code):
    user_code = user_code.strip()
    if not ALLOWED_CHARS.fullmatch(user_code):
        raise ValueError("Только латинские буквы/цифры, длина ≤16")
    if user_code in RESERVED:
        raise ValueError(
            "Предложенный вариант короткой ссылки уже существует.")
    return user_code


def generate_short_link(short_code):
    short_link = request.url_root + short_code
    return short_link