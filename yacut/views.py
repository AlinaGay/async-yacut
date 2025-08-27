import asyncio
import aiohttp
from random import randrange
from flask import abort, flash, redirect, render_template, request, url_for

from . import app, db
from .forms import FileUploadForm
from .models import URLMap
from .utils import generate_short_code, generate_short_link
from .yadisk import upload_files_to_yadisk


@app.route('/upload', methods=['GET', 'POST'])
async def file_upload_view():
    form = FileUploadForm()
    if form.validate_on_submit():
        results = await upload_files_to_yadisk(form.files.data)
        pairs = []
        for filename, url in results:
            short_code = generate_short_code()
            db.session.add(URLMap(
                original=url,
                short=short_code
            ))
            short_link = generate_short_link(short_code)
            pairs.append({"filename": filename, "url": short_link})

        db.session.commit()
        print(pair.filename for pair in pairs)
        return render_template('file.html', form=form, pairs=pairs)
    return render_template('file.html', form=form)
