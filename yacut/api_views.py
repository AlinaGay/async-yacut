from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import (
    ALLOWED_CHARS, RESERVED,
    generate_short_link,
    get_unique_short_id
)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True) or {}
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)

    original_url = (data.get('url') or '').strip()
    if not original_url:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)

    short_code = data.get('custom_id')
    if (short_code in RESERVED) or (not ALLOWED_CHARS.fullmatch(short_code)):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки', 400)
    if URLMap.query.filter_by(short=short_code).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.', 400)
    if not short_code:
        short_code = get_unique_short_id()

    db.session.add(URLMap(original=original_url, short=short_code))
    db.session.commit()
    short_link = generate_short_link(short_code)
    return jsonify({"url": original_url, "short_link": short_link}), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_map.original}), 200