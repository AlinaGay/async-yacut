"""Application configuration for the YaCut service.

This module defines the `Config` class, which loads environment-based
settings for the Flask application, including:

- Database connection URI.
- Secret key for session and CSRF protection.
- OAuth token for Yandex Disk API integration.
"""

import os


class Config(object):
    """Base configuration class for the Flask application."""

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DISK_TOKEN = os.getenv("DISK_TOKEN")
