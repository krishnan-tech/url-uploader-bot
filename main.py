import logging
import os
from dotenv import load_dotenv
from config import Config as SETTING
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import siaskynet as skynet

load_dotenv()
client = skynet.SkynetClient()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

TOKEN = os.getenv("TOKEN")

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    text = """Hello there 👋\nThis bot is made by @Kishnan_Navadia and @MrGrey126
    """
    update.message.reply_text(text)

def upload_siasky(file_path):
    skylink = client.upload_file(file_path)
    return SETTING.SIASKY_CLIENT + skylink[6:]

def create_upload_folder():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

def remove_uploaded_file(file_name):
    os.remove(f'uploads/{file_name}') # delete downloaded file from server

def main_function(update: Update, context: CallbackContext) -> None:
    # ['text', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'message_auto_delete_timer_changed', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'poll', 'dice', 'passport_data', 'proximity_alert_triggered', 'voice_chat_scheduled', 'voice_chat_started', 'voice_chat_ended', 'voice_chat_participants_invited', 'audio', 'game', 'animation', 'document', 'photo', 'sticker', 'video', 'voice', 'video_note', 'contact', 'location', 'venue', 'invoice', 'successful_payment']

    # if input is photo
    if len(update.message.photo) > 0:

        create_upload_folder() # create upload folder if not exists
        file_unique_id = (update.message.photo[-1]['file_unique_id']) # get file ID
        
        update.message.reply_text("Image Downloading... 😎")
        update.message.photo[-1].get_file().download(f"uploads/{file_unique_id}") # download image

        update.message.reply_text("Image Uploading... 📤")
        update.message.reply_text(f"{SETTING.PHOTO_MSG}\n{upload_siasky(f'uploads/{file_unique_id}')}") # upload image

        remove_uploaded_file(file_unique_id)
    
    # if input is video
    elif update.message.video != None:

        create_upload_folder() # create upload folder if not exists
        file_unique_id = (update.message.video['file_unique_id']) # get file ID

        update.message.reply_text("Video Downloading... 😎")
        update.message.video.get_file().download(f"uploads/{file_unique_id}") # download video

        update.message.reply_text("Video Uploading... 📤")
        update.message.reply_text(f"{SETTING.VIDEO_MSG}\n{upload_siasky(f'uploads/{file_unique_id}')}") # upload video

        remove_uploaded_file(file_unique_id)

    # if input is document
    elif update.message.document != None:

        create_upload_folder() # create upload folder if not exists
        file_unique_id = (update.message.document['file_unique_id']) # get file ID

        update.message.reply_text("File Downloading... 😎")
        update.message.document.get_file().download(f"uploads/{file_unique_id}") # download file

        update.message.reply_text("File Uploading... 📤")
        update.message.reply_text(f"{SETTING.DOCUMENT_MSG}\n{upload_siasky(f'uploads/{file_unique_id}')}") # upload file

        remove_uploaded_file(file_unique_id)

    # if input is audio
    elif update.message.audio != None:

        create_upload_folder() # create upload folder if not exists
        file_unique_id = (update.message.audio['file_unique_id']) # get file id

        update.message.reply_text("Audio Downloading... 😎")
        update.message.audio.get_file().download(f"uploads/{file_unique_id}") # download file

        update.message.reply_text("Audio Uploading... 📤")
        update.message.reply_text(f"{SETTING.AUDIO_MSG}\n{upload_siasky(f'uploads/{file_unique_id}')}") # upload audio

        remove_uploaded_file(file_unique_id)

    # TODO : Refactor code

    # TODO : Bot is limited 50mb for document and 20mb for others



def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(None, main_function))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()