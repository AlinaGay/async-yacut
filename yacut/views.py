import io
import requests
from flask import flash, redirect, render_template, send_file
from werkzeug.urls import iri_to_uri

from . import app, db
from .forms import FileUploadForm, ShortLinkForm
from .models import URLMap
from .utils import (
    generate_short_link,
    get_filename_from_url,
    get_unique_short_id,
    is_yandex_disk_link,
    validate_user_code
)
from .yadisk import upload_files_to_yadisk


@app.route('/', methods=['GET', 'POST'])
def link_cut_view():
    form = ShortLinkForm()

    if form.validate_on_submit():
        original_link = form.original_link.data

        if form.custom_id.data:
            try:
                short_code = validate_user_code(form.custom_id.data)
            except ValueError as e:
                flash(str(e), 'error')
                return render_template('link.html', form=form)
        else:
            short_code = get_unique_short_id()

        db.session.add(URLMap(
            original=original_link,
            short=short_code
        ))
        db.session.commit()
        short_link = generate_short_link(short_code)
        return render_template('link.html', form=form, url=short_link)
    return render_template('link.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def file_upload_view():
    form = FileUploadForm()
    if form.validate_on_submit():
        results = await upload_files_to_yadisk(form.files.data)
        pairs = []
        for filename, url in results:
            short_id = get_unique_short_id()
            db.session.add(URLMap(
                original=url,
                short=short_id
            ))
            short_link = generate_short_link(short_id)
            pairs.append({"filename": filename, "url": short_link})

        db.session.commit()
        return render_template('file.html', form=form, pairs=pairs)
    return render_template('file.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    original_url = url_map.original

    if not is_yandex_disk_link(original_url):
        return redirect(iri_to_uri(original_url), code=302)

    try:
        with requests.get(original_url, stream=True, timeout=10) as response:
            response.raise_for_status()

            return send_file(
                io.BytesIO(response.content),
                as_attachment=True,
                download_name=get_filename_from_url(
                    original_url, f"file_{short_id}"),
                mimetype=response.headers.get('content-type')
            )

    except requests.RequestException:
        return redirect(iri_to_uri(original_url), code=302)
