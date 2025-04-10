import logging
from struct import pack
import re
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import DATABASE_URL, DATABASE_NAME, COLLECTION_NAME, MAX_BTN

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

async def save_file(message):

    """Save file in database"""



    media = None

    for attr in ["document", "video", "audio", "photo"]:

        media = getattr(message, attr, None)

        if media:

            break



    if not media:

        print("Unsupported media type")

        return 'err'



    try:

        file_id = unpack_new_file_id(media.file_id)

    except Exception as e:

        print(f"Failed to unpack file_id: {e}")

        return 'err'



    # Use filename fallback if not available

    file_name = getattr(media, 'file_name', None) or f"{media.file_unique_id}"

    file_name = re.sub(r"@\w+|(_|\-|\.|\+)", " ", str(file_name))



    # Caption only exists on message, not on media object

    file_caption = re.sub(r"@\w+|(_|\-|\.|\+)", " ", str(getattr(message, 'caption', '')))



    try:

        file = Media(

            file_id=file_id,

            file_name=file_name,

            file_size=getattr(media, 'file_size', 0),

            caption=file_caption

        )

    except ValidationError:

        print(f'Saving Error - {file_name}')

        return 'err'

    else:

        try:

            await file.commit()

        except DuplicateKeyError:

            print(f'Already Saved - {file_name}')

            return 'dup'

        else:

            print(f'Saved - {file_name}')

            return 'suc'
