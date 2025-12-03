from telegram import Bot

# Configuration
BOT_TOKEN = "8397682707:AAGyTrnumyd3TIu8lfErnbZoOdXAVRUUt_0"
CHAT_ID = "-1003208146639"

# Initialize Telegram bot
bot = Bot(token=BOT_TOKEN)

# Sets to track downloaded items
downloaded_items_yts = set()
downloaded_items_tg = set()
