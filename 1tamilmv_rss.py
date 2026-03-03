import feedparser
import re

RSS_URL = "https://www.1tamilmv.gs/rss"

def fetch_1tamilmv():
    feed = feedparser.parse(RSS_URL)
    posts = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = entry.get("summary", "")

        # 🔗 MAGNET extract
        magnet = None
        magnet_match = re.search(r'href="(magnet:\?xt=.*?)"', summary)
        if magnet_match:
            magnet = magnet_match.group(1)

        # 🎞 Quality extract
        quality = "HDRip"
        q_match = re.search(r'(480p|720p|1080p|2160p|4K)', title, re.I)
        if q_match:
            quality = q_match.group(1)

        if magnet:
            posts.append({
                "title": title,
                "quality": quality,
                "magnet": magnet,
                "source": "1TamilMV",
                "link": link
            })

    return posts
