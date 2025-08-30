"""Form definitions for the YaCut URL-shortening service.

This module provides two Flask-WTF forms:

- `ShortLinkForm`: Form for creating a short link from a long URL,
  with optional custom short code input.
- `FileUploadForm`: Form for uploading multiple files to Yandex Disk,
  restricted to a set of allowed file types.

Both forms use WTForms validators to enforce input constraints and
provide user-friendly error messages.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    ORIGINAL_MAX_LENGTH,
    CUSTOM_ID_MAX_LENGTH
)


class ShortLinkForm(FlaskForm):
    """Form for submitting an original URL and an optional custom short ID."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(
            message='Обязательное поле'), Length(max=ORIGINAL_MAX_LENGTH)],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=CUSTOM_ID_MAX_LENGTH),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Только латинские буквы и цифры'
            )
        ],
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    """Form for uploading multiple files to Yandex Disk."""

    files = MultipleFileField(
        'Файл не выбран',
        validators=[
            FileAllowed(
                [
                    'jpg', 'jpeg', 'png', 'gif', 'bmp',
                    'txt', 'py', 'pdf', 'docx', 'xlsx',
                    'csv', 'md', 'rtf',
                    'mp3', 'wav',
                    'mp4', 'avi', 'mov',
                    'zip', 'rar', '7z'
                ],
                message=(
                    'Выберите файлы с расширением: '
                    '.jpg, .jpeg, .png, .gif, .bmp, '
                    '.txt, .py, .pdf, .docx, .xlsx, .csv, .md, .rtf, '
                    '.mp3, .wav, .mp4, .avi, .mov, '
                    '.zip, .rar, .7z'
                )
            )
        ]
    )
    submit = SubmitField('Загрузить')