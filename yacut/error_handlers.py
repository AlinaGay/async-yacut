"""Application-level error handling for the Flask project.

This module defines:
- A custom exception class `InvalidAPIUsage` for returning JSON API errors.
- Error handlers that serialize API errors to JSON and render HTML pages
  for common HTTP errors (404 and 400).
"""

from flask import jsonify, render_template

from . import app, db


class APIUsageError(Exception):
    """Exception to represent a client-facing API error (HTTP 4xx)."""

    status_code = 400

    def __init__(self, message, status_code=None):
        """Initialize the exception."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Return a serializable payload for JSON responses."""
        return dict(message=self.message)


@app.errorhandler(APIUsageError)
def invalid_api_usage(error):
    """Convert an `InvalidAPIUsage` exception into a JSON HTTP response."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Render the HTML page for 404 Not Found."""
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request(error):
    """Render the HTML page for 400 Bad Request."""
    db.session.rollback()
    return render_template('400.html'), 400
