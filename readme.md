### YaCut — URL Shortening and Yandex.Disk File Upload Service

YaCut is a Flask application that allows you to:
- Create short links for any URL.
- Upload files to Yandex.Disk and get short links for direct downloads.
- Use a short identifier for quick access to the original resource.

## Features

- URL shortening — Enter any URL and the service generates a short identifier.
- File uploads — Upload multiple files at once; files are stored on Yandex.Disk and the user receives short download links.
- Redirects and proxy — Following a short link either redirects to the original URL or serves a file from Yandex.Disk.
- Asynchronous interaction with the Yandex.Disk API — Uses aiohttp and asyncio for parallel file uploads.
- Secure connections — All requests are made over TLS/SSL with trusted certificates via certifi.
  
## Main Routes

- / — Form for URL shortening.
- /files — Form for uploading files to Yandex.Disk and obtaining short download links.
- /<short_id> — Redirect via the short link (either to the original URL or to file download).

## Technologies

- Flask — Web framework.
- SQLAlchemy — Stores link data.
- WTForms — Form validation.
- aiohttp, asyncio — Asynchronous requests to the Yandex.Disk API.
- certifi — Trusted certificates for HTTPS.

### How to Run the Yacut Project

Clone the repository and navigate into it in the command line:

```
git clone 
```

```
cd yacut
```

Create and activate a virtual environment:

```
python3 -m venv venv
```

* For Linux/macOS

    ```
    source venv/bin/activate
    ```

* For Windows

    ```
    source venv/scripts/activate
    ```

Install the dependencies from the requirements.txt file:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Create a .env file in the project directory with the following four environment variables:

```
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DB=sqlite:///db.sqlite3
```

Create the database and apply the migrations:

```
flask db upgrade
```

Start the project:

```
flask run
```
