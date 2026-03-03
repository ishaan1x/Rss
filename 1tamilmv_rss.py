import feedparser
import asyncio
import re
from telegram.constants import ParseMode
from config import bot, CHAT_ID, downloaded_items_tg


async def fetch_and_post_1tamilmv_feeds():
    """Fetch 1TamilMV RSS feeds and post new items to Telegram"""
    try:
        feed = feedparser.parse("https://www.1tamilmv.gs/rss")

        if not feed.entries:
            print("No entries found in the 1TamilMV RSS feed.")
            return

        for item in feed.entries:
            title = item.get("title", "No Title")
            link = item.get("link", "")
            summary = item.get("summary", "")

            # 🧲 MAGNET extract
            magnet = None
            magnet_match = re.search(r'href="(magnet:\?xt=.*?)"', summary)
            if magnet_match:
                magnet = magnet_match.group(1)

            if not magnet:
                continue

            # 🎞 Quality extract
            quality = "HDRip"
            q_match = re.search(r'(480p|720p|1080p|2160p|4K)', title, re.I)
            if q_match:
                quality = q_match.group(1)

            # Duplicate check
            if magnet in downloaded_items_tg:
                continue

            # 📨 Telegram Message
            message = (
                f"🎬 <b>[{quality}] {title}</b>\n\n"
                f"🧲 <b>MAGNET:</b>\n<code>{magnet}</code>\n\n"
                f"🌐 https://tghubfile.pages.dev"
            )

            await bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )

            downloaded_items_tg.add(magnet)
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error in 1TamilMV feed handling: {e}")
