from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class ShortLinkForm(FlaskForm):
    original_link = URLField(
        'Введите адрес длинной ссылки',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 256)],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()],
    )
    submit = SubmitField('Создать')


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        validators=[
            FileAllowed(
                ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'txt', 'py'],
                message=(
                    'Выберите файлы с расширением '
                    '.jpg, .jpeg, .png, .gif, .txt, .py или .bmp'
                )
            )
        ]
    )
    submit = SubmitField('Загрузить')