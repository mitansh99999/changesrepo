from info import BIN_CHANNEL, URL, SHOW_ADS
from utils import temp
from web.utils.custom_dl import TGCustomYield
from database.users_chats_db import db
import urllib.parse
import aiofiles
import aiohttp

AD_SCRIPT = "<script type='text/javascript' src='//pl24249468.cpmrevenuegate.com/e8/17/6d/e8176d0f0a248f9364dfe3b5f43b5c47.js'></script>"

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
            
            # Insert ad content into the placeholder
            html = html.replace('<div class="ad-container">', f'<div class="ad-container">{AD_SCRIPT}')
    
    return html
