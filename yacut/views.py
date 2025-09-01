"""Flask views for the YaCut URL-shortening service.

This module exposes three routes:
- `link_cut_view` ("/"): HTML form to create short links for arbitrary URLs.
- `file_upload_view` ("/files"): Async handler that uploads multiple files to
  Yandex Disk and returns short links pointing to downloadable resources.
- `redirect_view` ("/<short_id>"): Resolves a short ID to the original URL
  and either redirects (generic URLs)
  or proxies the file download (Yandex Disk).
"""

from flask import flash, redirect, render_template
from werkzeug.urls import iri_to_uri

from . import app, db
from .forms import FileUploadForm, ShortLinkForm
from .models import URLMap
from .utils import generate_short_link
from .yadisk import upload_files_to_yadisk


@app.route('/', methods=['GET', 'POST'])
def link_cut_view():
    """Render the main page and handle creation of short links."""
    form = ShortLinkForm()

    if form.validate_on_submit():
        try:
            obj = URLMap.validate_user_code(
                original_url=form.original_link.data,
                custom_id=form.custom_id.data,
            )
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('link.html', form=form)
        return render_template(
            'link.html', form=form, url=generate_short_link(obj.short))
    return render_template('link.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def file_upload_view():
    """Upload multiple files to Yandex Disk and return short links."""
    form = FileUploadForm()
    if form.validate_on_submit():
        results = await upload_files_to_yadisk(form.files.data)
        pairs = []
        for filename, url in results:
            short_id = URLMap.get_unique_short_id()
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
    """
    Resolve a short ID to the original URL.

    Deliver content to the client.
    """
    url_obj = URLMap.query.filter_by(short=short_id).first_or_404()
    original_url = url_obj.original

    return redirect(iri_to_uri(original_url), code=302)
