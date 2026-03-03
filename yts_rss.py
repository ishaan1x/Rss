import feedparser
import asyncio
from telegram.constants import ParseMode
from config import bot, CHAT_ID, downloaded_items_yts

async def fetch_and_post_yts_feeds():
    """Fetch YTS RSS feeds and post new items to Telegram"""
    try:
        # Fetch RSS feed
        feed = feedparser.parse("https://yts.bz/rss/")
        if not feed.entries:
            print("No entries found in the YTS RSS feed.")
            return

        # Process each feed entry
        for item in feed.entries:
            title = item.get("title", "No Title")
            link = item.get("link", "")
            magnet_link = item.links[1].href if len(item.links) > 1 else None
            torrent_file = item.enclosures[0].href if item.enclosures else None

            if link not in downloaded_items_yts:
                # Construct message
                message = f"🎥 <b>{title}</b>\n\n"
                if torrent_file:
                    message += f"🔗 <b>Torrent File:</b> <a href='{torrent_file}'>Download</a>\n"
                if magnet_link:
                    message += f"🧲 <b>Magnet Link:</b>\n<code>{magnet_link}</code>\n\n"
                    message += f"🌐 <b>Source:</b> <a href='{link}'>YTS</a>"

                # Send message to Telegram
                await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)
                downloaded_items_yts.add(link)
                await asyncio.sleep(1)

    except Exception as e:
        print(f"Error in YTS feed handling: {e}")
