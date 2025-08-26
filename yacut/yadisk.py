import asyncio
import ssl, certifi, aiohttp
import urllib

from . import app


AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'

DISK_INFO_URL = f'{API_HOST}{API_VERSION}/disk/'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


ssl_ctx = ssl.create_default_context(cafile=certifi.where())


async def upload_files_to_yadisk(files):
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_ctx)
        ) as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, file)
                    )
                )
                urls = await asyncio.gather(*tasks)
            return urls


async def upload_file_and_get_url(session, file):
    print('type:         ', file.filename)
    payload = {
        'path': f'app:/{file.filename}',
        'overwrite': 'True'
    }
    async with session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    ) as response_1:
        data = await response_1.json()
        upload_url = data['href']

    file_content = file.read()

    async with session.put(
        data=file_content,
        url=upload_url,
    ) as response_2:
        location = response_2.headers['Location']
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')

    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': f'{location}'}
    ) as response_3:
        data = await response_3.json()
        link = data['href']
    return link
