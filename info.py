import re, logging
from os import environ
from Script import script

def is_enabled(type, value):
    data = environ.get(type, str(value))
    if data.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif data.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        print(f'Error - {type} is invalid, exiting now')
        exit()

def is_valid_ip(ip):
    ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    return re.match(ip_pattern, ip) is not None

# Bot information
API_ID = environ.get('API_ID', '15503725')  #api id of your telegram id
if len(API_ID) == 0:
    print('Error - API_ID is missing, exiting now')
    exit()
else:
    API_ID = int(API_ID)
API_HASH = environ.get('API_HASH', 'd11e4a03659488e40429f3c39431b6db') #api hash of your telegram id
if len(API_HASH) == 0:
    print('Error - API_HASH is missing, exiting now')
    exit()
BOT_TOKEN = environ.get('BOT_TOKEN', '6131871030:AAG06XYWVFLLgXhJiwSGzo_hEgMkj08jfr8') #bot token from botfather
if len(BOT_TOKEN) == 0:
    print('Error - BOT_TOKEN is missing, exiting now')
    exit()
PORT = int(environ.get('PORT', '80')) #don't change anything 

# Bot pics
PICS = (environ.get('PICS', 'https://telegra.ph/file/58fef5cb458d5b29b0186.jpg https://telegra.ph/file/f0aa4f433132769f8970c.jpg https://telegra.ph/file/f515fbc2084592eca60a5.jpg https://telegra.ph/file/20dbdcffaa89bd3d09a74.jpg https://telegra.ph/file/6045ba953af4def846238.jpg')).split()

# Bot Admins
ADMINS = environ.get('ADMINS', '1398885416 767386502') #apni tg id daalo
if len(ADMINS) == 0:
    print('Error - ADMINS is missing, exiting now')
    exit()
else:
    ADMINS = [int(admins) for admins in ADMINS.split()]

# Channels
INDEX_CHANNELS = [int(index_channels) if index_channels.startswith("-") else index_channels for index_channels in environ.get('INDEX_CHANNELS', '-1001242070400 -1001727262090 -1001896431744').split()]
if len(INDEX_CHANNELS) == 0:
    print('Info - INDEX_CHANNELS is empty')
AUTH_CHANNEL = [int(auth_channels) for auth_channels in environ.get('AUTH_CHANNEL', '').split()]
if len(AUTH_CHANNEL) == 0:
    print('Info - AUTH_CHANNEL is empty')
LOG_CHANNEL = environ.get('LOG_CHANNEL', '-1001602859617') #bot log channel -1005293546253
if len(LOG_CHANNEL) == 0:
    print('Error - LOG_CHANNEL is missing, exiting now')
    exit()
else:
    LOG_CHANNEL = int(LOG_CHANNEL)
IS_FSUB = is_enabled('IS_FSUB', True)

# support group
SUPPORT_GROUP = environ.get('SUPPORT_GROUP', '-1001816890116') #support group id ex:  -1002936246860
if len(SUPPORT_GROUP) == 0:
    print('Error - SUPPORT_GROUP is missing, exiting now')
    exit()
else:
    SUPPORT_GROUP = int(SUPPORT_GROUP)

# MongoDB information
DATABASE_URL = environ.get('DATABASE_URL', "mongodb+srv://md:md@cluster0.kznetvq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") #mongo db url
if len(DATABASE_URL) == 0:
    print('Error - DATABASE_URL is missing, exiting now')
    exit()
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Files')

# Links
SUPPORT_LINK = environ.get('SUPPORT_LINK', 'https://t.me/MrLatestMoviesbot')
UPDATES_LINK = environ.get('UPDATES_LINK', 'https://t.me/Theprofffesorr')
FILMS_LINK = environ.get('FILMS_LINK', 'https://t.me/+3w9JlpDFFJ85MmI9')
TUTORIAL = environ.get("TUTORIAL", "https://t.me/HowToDownloadOurSite/9")
VERIFY_TUTORIAL = environ.get("VERIFY_TUTORIAL", "https://t.me/HowToDownloadOurSite/9")

# Bot settings
DELETE_TIME = int(environ.get('DELETE_TIME', 3600)) # Add time in seconds 
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
MAX_BTN = int(environ.get('MAX_BTN', 10)) #don't change anything in Language 
LANGUAGES = [language.lower() for language in environ.get('LANGUAGES', 'english hindi telugu tamil kannada malayalam').split()]
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", script.IMDB_TEMPLATE)
FILE_CAPTION = environ.get("FILE_CAPTION", script.FILE_CAPTION)
SHORTLINK_URL = environ.get("SHORTLINK_URL", "droplink.co")
SHORTLINK_API = environ.get("SHORTLINK_API", "e3db093b5ee80c49597b6a30160a541d8e33b1dc")
VERIFY_EXPIRE = int(environ.get('VERIFY_EXPIRE', 18000)) # Add time in seconds
WELCOME_TEXT = environ.get("WELCOME_TEXT", script.WELCOME_TEXT)
INDEX_EXTENSIONS = [extensions.lower() for extensions in environ.get('INDEX_EXTENSIONS', 'mp4 mkv').split()]
STICKERS_IDS = (
    "CAACAgQAAxkBAAEK99dlfC7LDqnuwtGRkIoacot_dGC4zQACbg8AAuHqsVDaMQeY6CcRojME CAACAgQAAxkBAAELqxll8CcG-MZx9mIOXgaHSzLc9uyxswACaxQAAlrdEVOJDG3cIZuWLzQE"
).split()

# boolean settings 
GROUP_FSUB = is_enabled('GROUP_FSUB', False) 
PM_SEARCH = is_enabled('PM_SEARCH', False) #switch True or False for searching results in bot pm😃
IS_VERIFY = is_enabled('IS_VERIFY', True)
AUTO_DELETE = is_enabled('AUTO_DELETE', False)
WELCOME = is_enabled('WELCOME', True)
PROTECT_CONTENT = is_enabled('PROTECT_CONTENT', False)
LONG_IMDB_DESCRIPTION = is_enabled("LONG_IMDB_DESCRIPTION", False)
LINK_MODE = is_enabled("LINK_MODE", True)
AUTO_FILTER = is_enabled('AUTO_FILTER', True)
IMDB = is_enabled('IMDB', True)
SPELL_CHECK = is_enabled("SPELL_CHECK", True)
SHORTLINK = is_enabled('SHORTLINK', False)


PAYMENT_QR = environ.get('PAYMENT_QR', 'https://telegra.ph/file/e1d10fb7d6a3c211f3fb9.jpg') #telegraph link of your QR code 
UPI_ID = environ.get('UPI_ID', 'mitanshdhiman0001@okicici') # Add your upi id here
# for stream
IS_STREAM = is_enabled('IS_STREAM', True) #true if you want stream feature active in your bot
BIN_CHANNEL = environ.get("BIN_CHANNEL", "-1001346044919") #if is_stream = true then add a channel id ex: -10026393639
if len(BIN_CHANNEL) == 0:
    print('Error - BIN_CHANNEL is missing, exiting now')
    exit()
else:
    BIN_CHANNEL = int(BIN_CHANNEL)
URL = environ.get("URL", "https://auto-filter-bot-279f.onrender.com") #if heroku then paste the app link here ex: https://heroku......./
if len(URL) == 0:
    print('Error - URL is missing, exiting now')
    exit()
else:
    if URL.startswith(('https://', 'http://')):
        if not URL.endswith("/"):
            URL += '/'
    elif is_valid_ip(URL):
        URL = f'http://{URL}/'
    else:
        print('Error - URL is not valid, exiting now')
        exit()
