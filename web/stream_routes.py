import time
import math
import logging
import secrets
import mimetypes
from info import BIN_CHANNEL
from utils import temp
from aiohttp import web
from web.utils.custom_dl import TGCustomYield, chunk_size, offset_fix
from web.utils.render_template import media_watch
from urllib.parse import quote_plus
import logging

logging.basicConfig(level=logging.INFO)

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
        html_content = '''
    <html>
    <head>
        <title>Welcome to Theproffessor x Movies Zone</title>
        <style>
            body {
                background-color: #121212;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            .container {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            a {
                color: #1DB954;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
            .button {
                background-color: #1DB954;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin-top: 20px;
                border-radius: 25px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #1ed760;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to <a href="https://t.me/+3w9JlpDFFJ85MmI9">𝚃𝚑𝚎𝚙𝚛𝚘𝚏𝚏𝚏𝚎𝚜𝚘𝚛𝚛 𝚡 𝙼𝚘𝚟𝚒𝚎𝚜 𝚉𝚘𝚗𝚎</a></h1>
            <p>Your hub for the latest movies and shows.</p>
            <a class="button" href="https://t.me/+3w9JlpDFFJ85MmI9">Join Us</a>
        </div>
    </body>
    </html>
    '''
        return web.Response(text=html_content, content_type='text/html')


@routes.get("/watch/{message_id}")
async def watch_handler(request):
    try:
        # Attempt to parse the message ID
        message_id = int(request.match_info['message_id'])
        # Call your media_watch function
        response_text = await media_watch(message_id)
        return web.Response(text=response_text, content_type='text/html')
    except ValueError:
        # Log and handle the case where message_id is not an integer
        logging.error("Invalid message_id: must be an integer")
        return web.Response(text="<h1>Invalid message ID</h1>", content_type='text/html')
    except Exception as e:
        # Log any other exceptions for further investigation
        logging.exception("An error occurred while processing the request")
        return web.Response(text="<h1>Something went wrong</h1>", content_type='text/html')

@routes.get("/download/{message_id}")
async def download_handler(request):
    try:
        message_id = int(request.match_info['message_id'])
        return await media_download(request, message_id)
    except:
        return web.Response(text="<h1>Something went wrong</h1>", content_type='text/html')
        

async def media_download(request, message_id: int):
    range_header = request.headers.get('Range', 0)
    media_msg = await temp.BOT.get_messages(BIN_CHANNEL, message_id)
    file_properties = await TGCustomYield().generate_file_properties(media_msg)
    file_size = file_properties.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace('bytes=', '').split('-')
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = request.http_range.stop or file_size - 1

    req_length = until_bytes - from_bytes

    new_chunk_size = await chunk_size(req_length)
    offset = await offset_fix(from_bytes, new_chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = (until_bytes % new_chunk_size) + 1
    part_count = math.ceil(req_length / new_chunk_size)
    body = TGCustomYield().yield_file(media_msg, offset, first_part_cut, last_part_cut, part_count,
                                      new_chunk_size)

    file_name = file_properties.file_name if file_properties.file_name \
        else f"{secrets.token_hex(2)}.jpeg"
    mime_type = file_properties.mime_type if file_properties.mime_type \
        else f"{mimetypes.guess_type(file_name)}"

    return_resp = web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": mime_type,
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        }
    )

    if return_resp.status == 200:
        return_resp.headers.add("Content-Length", str(file_size))

    return return_resp
