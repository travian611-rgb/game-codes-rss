import requests
from bs4 import BeautifulSoup
import datetime

pages = {
    "Wuthering Waves": "https://www.pcgamesn.com/wuthering-waves/codes",
    "Honkai Star Rail": "https://www.pcgamesn.com/honkai-star-rail/codes",
    "Zenless Zone Zero": "https://www.pcgamesn.com/zenless-zone-zero/codes"
}

items = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for game, url in pages.items():
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Look for list entries that contain <strong>
    for li in soup.find_all("li"):
        strong = li.find("strong")
        if not strong:
            continue

        code = strong.get_text(strip=True)
        if len(code) < 4:  # filter out garbage
            continue

        # Reward is rest of li text minus code
        full = li.get_text(" ", strip=True)
        reward = full.replace(code, "").strip(" -–:")

        items.append({
            "title": f"{code} ({game})",
            "description": reward,
            "link": f"{url}?code={code}"
        })

# Build RSS
rss_items = "\n".join([
    f"""<item>
<title>{i['title']}</title>
<description><![CDATA[{i['description']}]]></description>
<link>{i['link']}</link>
</item>"""
    for i in items
])

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>Game Codes Feed</title>
<link>https://travian611-rgb.github.io/game-codes-rss/codes.xml</link>
<description>Automatically updated game codes</description>
<lastBuildDate>{datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
{rss_items}
</channel>
</rss>
"""

with open("codes.xml", "w", encoding="utf-8") as f:
    f.write(rss)
