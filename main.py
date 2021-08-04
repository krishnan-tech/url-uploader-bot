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
    return skylink[6:]

def main_function(update: Update, context: CallbackContext) -> None:
    # ['text', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'message_auto_delete_timer_changed', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'poll', 'dice', 'passport_data', 'proximity_alert_triggered', 'voice_chat_scheduled', 'voice_chat_started', 'voice_chat_ended', 'voice_chat_participants_invited', 'audio', 'game', 'animation', 'document', 'photo', 'sticker', 'video', 'voice', 'video_note', 'contact', 'location', 'venue', 'invoice', 'successful_payment']

    # if input is photo
    if len(update.message.photo) > 0:

        if not os.path.exists("photos"):
            os.makedirs("photos")

        file_unique_id = (update.message.photo[-1]['file_unique_id']) # get file ID
        
        update.message.reply_text("Image Downloading... 😎")
        update.message.photo[-1].get_file().download(f"photos/{file_unique_id}") # download image

        update.message.reply_text("Image Uploading... 📤")
        update.message.reply_text(f"{SETTING.PHOTO_MSG}\n{SETTING.SIASKY_CLIENT}{upload_siasky(f'photos/{file_unique_id}')}") # upload image

        os.remove(f'photos/{file_unique_id}') # delete downloaded image from server
    
    # if input is video
    elif update.message.video != None:

        if not os.path.exists("videos"):
            os.makedirs("videos")

        file_unique_id = (update.message.video['file_unique_id']) # get file ID

        update.message.reply_text("Video Downloading... 😎")
        update.message.video.get_file().download(f"videos/{file_unique_id}") # download video

        update.message.reply_text("Video Uploading... 📤")
        update.message.reply_text(f"{SETTING.VIDEO_MSG}\n{SETTING.SIASKY_CLIENT}{upload_siasky(f'videos/{file_unique_id}')}") # upload video

        os.remove(f'videos/{file_unique_id}') # delete downloaded video from server

    # if input is document
    elif update.message.document != None:

        if not os.path.exists("documents"):
            os.makedirs("documents")
        file_unique_id = (update.message.document['file_unique_id']) # get file ID

        update.message.reply_text("File Downloading... 😎")
        update.message.document.get_file().download(f"documents/{file_unique_id}") # download file

        update.message.reply_text("File Uploading... 📤")
        update.message.reply_text(f"{SETTING.DOCUMENT_MSG}\n{SETTING.SIASKY_CLIENT}{upload_siasky(f'documents/{file_unique_id}')}") # upload file

        os.remove(f'videos/{file_unique_id}') # delete downloaded document from server

    # if input is audio
    elif update.message.audio != None:

        if not os.path.exists("audios"):
            os.makedirs("audios")
        file_unique_id = (update.message.audio['file_unique_id']) # get file ID

        update.message.reply_text("Audio Downloading... 😎")
        update.message.audio.get_file().download(f"audios/{file_unique_id}") # download file

        update.message.reply_text("Audio Uploading... 📤")
        update.message.reply_text(f"{SETTING.AUDIO_MSG}\n{SETTING.SIASKY_CLIENT}{upload_siasky(f'audios/{file_unique_id}')}") # upload audio

        os.remove(f'audios/{file_unique_id}') # delete downloaded audio from server

    # TODO : Refactor code

    # TODO : Bot is limited 50mb for document and 20mb for others



def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(None, main_function))

    updater.start_polling()
    updater.idle()


def test():
    skylink = client.upload_file("image.jpg")
    print(skylink)
    skylink = client.upload_file("video.mp4")
    print(skylink)

if __name__ == '__main__':
    main()
    # test()