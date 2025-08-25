# import asyncio
# import aiohttp
# import json
import requests
import urllib

from . import app


AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
# GET-запрос с заголовком авторизации
DISK_INFO_URL = f'{API_HOST}{API_VERSION}/disk/'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


def upload_files_to_yadisk(files):
    urls = []
    for file in files:
        urls.append(upload_file_and_get_url(file))
    return urls


def upload_file_and_get_url(file):
    payload = {
        # Загрузить файл с названием filename.txt в папку приложения.
        'path': f'app:/{file.filename}',
        'overwrite': 'True'  # Если файл существует, перезаписать его.
    }
    response_1 = requests.get(
        headers=AUTH_HEADERS,  # Заголовок для авторизации.
        params=payload,  # Указать параметры.
        url=REQUEST_UPLOAD_URL
    )
    upload_url = response_1.json()['href']

    with open('requirements.txt', 'rb') as file:
        response = requests.put(
            data=file,
            url=upload_url,
        )
    location = response.headers['Location']
    location = urllib.parse.unquote(location)
    location = location.replace('/disk', '')

    response_2 = requests.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': f'{location}'}
    )
    link = response_2.json()['href']
    return link
