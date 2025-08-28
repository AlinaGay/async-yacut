"""Database model definitions for the YaCut URL shortening service.

This module defines the SQLAlchemy model `URLMap`, which stores
associations between long original URLs and their shortened identifiers.
"""

from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """
    SQLAlchemy model.

    It is representing a mapping between an original URL
    and its shortened identifier.
    """

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
