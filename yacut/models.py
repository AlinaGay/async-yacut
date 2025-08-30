"""Database model definitions for the YaCut URL shortening service.

This module defines the SQLAlchemy model `URLMap`, which stores
associations between long original URLs and their shortened identifiers.
"""

import random
import string
from datetime import datetime

from yacut import db
from .constants import (
    ALLOWED_CHARS,
    CUSTOM_ID_MAX_LENGTH,
    ORIGINAL_MAX_LENGTH,
    RESERVED
)


class URLMap(db.Model):
    """
    SQLAlchemy model.

    It is representing a mapping between an original URL
    and its shortened identifier.
    """

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(db.String(CUSTOM_ID_MAX_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # @classmethod
    # def get_unique_short_id(cls, length=6):
    #     characters = string.ascii_letters + string.digits
    #     max_attempts = 10
    #     for attempt in range(max_attempts):
    #         short_id = ''.join(random.choice(characters) for _ in range(length))
    #         if not cls.query.filter_by(short=short_id).first():
    #             return short_id
    #     return cls.get_unique_short_id(length + 1)

    # @classmethod
    # def validate_user_code(cls, custom_id):
    #     """Validate a user-provided custom short code."""
    #     code = custom_id.strip()
    #     if code:
    #         if not ALLOWED_CHARS.fullmatch(code):
    #             raise ValueError('Только латинские буквы/цифры, длина ≤16')
    #         if (
    #             (code in RESERVED) or
    #             cls.query.filter_by(short=code).first()
    #         ):
    #             raise ValueError(
    #                 'Предложенный вариант короткой ссылки уже существует.')

    #     else:
    #         code = cls._generate_unique_short_id()    

    #     obj = cls(original=original, short=code)
    #     db.session.add(obj)
    #     db.session.commit()
    #     return obj