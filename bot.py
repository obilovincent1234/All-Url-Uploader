import os
import threading
import logging
from pyrogram.raw.all import layer
from pyrogram import Client, idle, __version__
from flask import Flask
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Start Flask in a separate thread
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Koyeb (Bot is running)"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# Start the bot
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
    os.makedirs(Config.DOWNLOAD_LOCATION)

if not Config.BOT_TOKEN or not Config.API_ID or not Config.API_HASH:
    logger.error("Missing config values")
    quit(1)

bot = Client(
    "All-Url-Uploader",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=50,
    plugins=dict(root="plugins"),
)

bot.start()
logger.info("**Bot Started**")
logger.info("**Pyrogram Version:** %s \n**Layer:** %s", __version__, layer)
idle()
bot.stop()
logger.info("**Bot Stopped**")
