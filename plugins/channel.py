from pyrogram import Client, filters
from info import INDEX_CHANNELS, INDEX_EXTENSIONS
from database.ia_filterdb import save_file

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(INDEX_CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    media_file = message.document or message.video
    if not media_file:
        return

    file_name = getattr(media_file, 'file_name', '')
    if file_name.lower().endswith(tuple(INDEX_EXTENSIONS)):
        await save_file(message)
