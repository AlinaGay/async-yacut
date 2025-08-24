from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import FileUploadForm


@app.route('/upload', methods=['GET', 'POST'])
def file_upload_view():
    form = FileUploadForm()
    return render_template('file.html', form=form)