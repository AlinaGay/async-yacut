from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import FileUploadForm
from .models import URLMap
from .utils import generate_short_code
from .yadisk import upload_files_to_yadisk


@app.route('/upload', methods=['GET', 'POST'])
def file_upload_view():
    form = FileUploadForm()
    if form.validate_on_submit():
        urls = upload_files_to_yadisk(form.files.data)
        for url in urls:
            short_hash = generate_short_code()
            url_map = URLMap(
                original=url,
                short=short_hash
            )
            db.session.add(url_map)
            db.session.commit()
    return render_template('file.html', form=form)
