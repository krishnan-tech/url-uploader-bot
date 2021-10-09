import logging
import os
from dotenv import load_dotenv
from config import Config as SETTING
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import siaskynet as skynet
import urllib.request
import validators
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import audioProvider
from myspotify import spotify_fetch
import re
from youtube_downloader import extract_youtube_id, yt_download

load_dotenv()
client = skynet.SkynetClient()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)

logger = logging.getLogger(__name__)

def clear_uploads(dir):
    if os.path.exists(dir):
        for file in os.listdir(dir):
            os.remove(os.path.join(dir, file))

def start(update: Update, context: CallbackContext) -> None:
    text = """Hello there 👋\nThis bot is made by @Kishnan_Navadia and @MrGrey126"""
    update.message.reply_text(text)


def upload_siasky(file_path):
    skylink = client.upload_file(file_path)
    return SETTING.SIASKY_CLIENT + skylink[6:]

def create_upload_folder():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

def remove_uploaded_file(file_name):
    os.remove(f'uploads/{file_name}') # delete downloaded file from server

def sendMessageAndUpload(update: Update, file_, download_text, uploading_text, starter_text) -> None:
    create_upload_folder() # create upload folder if not exists
    file_unique_id = (file_['file_unique_id']) # get file ID
    
    first_message = update.message.reply_text(download_text)
    file_.get_file().download(f"uploads/{file_unique_id}") # download image

    first_message.edit_text(uploading_text)
    first_message.edit_text(f"{starter_text}\n{upload_siasky(f'uploads/{file_unique_id}')}") # upload image

    remove_uploaded_file(file_unique_id)

def uploadFromText(update: Update, file_, download_text, uploading_text, starter_text) -> None:
    create_upload_folder() # create upload folder if not exists
    file_unique_id = (update.message.message_id) # get file ID
    
    first_message = update.message.reply_text(download_text)
    with urllib.request.urlopen(file_) as f:
        with open(f"uploads/{file_unique_id}", "wb") as f2:
            f2.write(f.read())

    first_message.edit_text(uploading_text)
    first_message.edit_text(f"{starter_text}\n{upload_siasky(f'uploads/{file_unique_id}')}") # upload image

    remove_uploaded_file(file_unique_id)


def uploadYoutube(update: Update, youtube_url, download_text, uploading_text, starter_text, type) -> None:
    create_upload_folder() # create upload folder if not exists
    youtube_id = extract_youtube_id(youtube_url)
    first_message = update.message.reply_text(download_text)
    yt_download(youtube_url, type) # download youtube video

    first_message.edit_text(uploading_text)
    if type == 0:
        first_message.edit_text(f"{starter_text}\n{upload_siasky(f'uploads/{youtube_id}.mp4')}") # upload image
        remove_uploaded_file(f"{youtube_id}.mp4")
    elif type == 1:
        first_message.edit_text(f"{starter_text}\n{upload_siasky(f'uploads/{youtube_id}.mp3')}") # upload image
        remove_uploaded_file(f"{youtube_id}.mp3")



def main_function(update: Update, context: CallbackContext) -> None:
    # ['text', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'message_auto_delete_timer_changed', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'poll', 'dice', 'passport_data', 'proximity_alert_triggered', 'voice_chat_scheduled', 'voice_chat_started', 'voice_chat_ended', 'voice_chat_participants_invited', 'audio', 'game', 'animation', 'document', 'photo', 'sticker', 'video', 'voice', 'video_note', 'contact', 'location', 'venue', 'invoice', 'successful_payment']

    # if there is url
    if update.effective_message.text:
        try:
            # if only url 
            if validators.url(update.message.text):
                # check for spotify
                spot_url = re.findall(r"[\bhttps://open.\b]*spotify[\b.com\b]*[/:]*track[/:]*[A-Za-z0-9?=]+", update.message.text)
                youtube_url = re.findall(r"[\bhttps://youtube.com/watch?v=\b]*[A-Za-z0-9?=]+", update.message.text)

                # if spotify url found
                if spot_url != []:
                    # update.message.reply_text(spotify_fetch(spot_url[0]))
                    uploadYoutube(update, spotify_fetch(spot_url[0]), "Downloading Spotify Audio... 😎", "Uploading... 📤", SETTING.AUDIO_MSG, 1)
                elif youtube_url != []:
                    uploadYoutube(update, youtube_url[0], "Downloading Youtube Video... 😎", "Uploading... 📤", SETTING.VIDEO_MSG, 0)


                # if direct url
                else:
                    uploadFromText(update, update.effective_message.text,  "Downloading from url... 😎", "Uploading... 📤", SETTING.TEXT_MSG)
            else:
                raise Exception
        except Exception as e:
            # if there is no url or only text like thing
            print(e)
            bot.sendMessage(update.effective_user.id, "Please provide valid download link...")
        return
    
    # if input is photo
    if len(update.message.photo) > 0:
        sendMessageAndUpload(update, update.message.photo[-1],  "Image Downloading... 😎", "Image Uploading... 📤", SETTING.PHOTO_MSG)
        return
    
    # if input is video
    elif update.message.video != None:
        sendMessageAndUpload(update, update.message.video, "Video Downloading... 😎", "Video Uploading... 📤", SETTING.VIDEO_MSG)
        return

    # if input is document
    elif update.message.document != None:
        sendMessageAndUpload(update, update.message.document, "File Downloading... 😎", "File Uploading... 📤", SETTING.DOCUMENT_MSG)
        return

    # if input is audio
    elif update.message.audio != None:
        sendMessageAndUpload(update, update.message.audio, "Audio Downloading... 😎", "Audio Uploading... 📤", SETTING.AUDIO_MSG)
        return

    # TODO : Bot is limited 50mb for document and 20mb for others


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(None, main_function))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    clear_uploads("uploads")
    main()
