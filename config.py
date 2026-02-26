from telegram import Bot

# Configuration
BOT_TOKEN = "8620564950:AAEegBh58f0VQpX1IeEYMdZn2zl86X4p4xA"
CHAT_ID = "-1003845689752"

# Initialize Telegram bot
bot = Bot(token=BOT_TOKEN)

# Sets to track downloaded items
downloaded_items_yts = set()
downloaded_items_tg = set()
