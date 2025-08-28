from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class ShortLinkForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 256)],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=16),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Только латинские буквы и цифры'
            )
        ],
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
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