import logging
import os
from dotenv import load_dotenv

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

def main_function(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(update.message.text)

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, main_function))

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