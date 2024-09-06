from info import BIN_CHANNEL, URL
from utils import temp
from web.utils.custom_dl import TGCustomYield
from database.users_chats_db import db
import urllib.parse
import aiofiles
import aiohttp

async def media_watch(message_id, user_id=None):
    # Fetch the media message details
    media_msg = await temp.BOT.get_messages(BIN_CHANNEL, message_id)
    file_properties = await TGCustomYield().generate_file_properties(media_msg)
    file_name, mime_type = file_properties.file_name, file_properties.mime_type
    src = urllib.parse.urljoin(URL, f'download/{message_id}')
    tag = mime_type.split('/')[0].strip()

    # Initialize the HTML content
    html = '<h1>This is not streamable file</h1>'

    if tag == 'video':
        async with aiofiles.open('web/template/watch.html') as r:
            heading = 'Watch - {}'.format(file_name)
            html_template = await r.read()

            # Prepare final HTML
            html = html_template.replace('tag', tag) % (heading, file_name, src)
    
    return html
