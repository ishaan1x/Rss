import feedparser
import asyncio
import re
from telegram.constants import ParseMode
from config import bot, CHAT_ID, downloaded_items_tg


# ❌ Basic adult keyword filter (safe side)
ADULT_KEYWORDS = [
    "", "", "", "", "",
    "", ""
]


def is_safe_title(title: str) -> bool:
    title_lower = title.lower()
    return not any(word in title_lower for word in ADULT_KEYWORDS)


def extract_thumbnail(item):
    # Try media_thumbnail
    if "media_thumbnail" in item:
        return item.media_thumbnail[0].get("url")

    # Try media_content
    if "media_content" in item:
        return item.media_content[0].get("url")

    # Try image from summary
    summary = item.get("summary", "")
    match = re.search(r'<img[^>]+src="([^"]+)"', summary)
    if match:
        return match.group(1)

    return None


async def fetch_and_post_torrentgalaxy_feeds():
    """Fetch Pornrips RSS feeds and post new items to Telegram"""
    try:
        feed = feedparser.parse("https://pornrips.to/feed/torrents")

        if not feed.entries:
            print("No entries found in the Pornrips RSS feed.")
            return

        for item in feed.entries:
            title = item.get("title", "No Title")
            link = item.get("link", "")

            # ⛔ Adult safety check
            if not is_safe_title(title):
                continue

            if link in downloaded_items_tg:
                continue

            # 🖼 Thumbnail extract
            thumbnail_url = extract_thumbnail(item)

            # 📩 Message body
            caption = (
                f"🎥 <b>{title}</b>\n\n"
                f"🧲 <b>Magnet Link:</b>\n<code>{link}</code>\n\n"
                f"🌐 <b>Source:</b> https://tghubfile.pages.dev"
            )

            try:
                # 📸 If thumbnail exists → send photo
                if thumbnail_url:
                    await bot.send_photo(
                        chat_id=CHAT_ID,
                        photo=thumbnail_url,
                        caption=caption,
                        parse_mode=ParseMode.HTML
                    )
                else:
                    # 📝 Fallback text message
                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=caption,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
                    )
            except Exception:
                # 🔁 Final fallback (Telegram image fail)
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=caption,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )

            downloaded_items_tg.add(link)
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error in Pornrips feed handling: {e}")
