import requests
from bs4 import BeautifulSoup
import datetime

pages = {
    "Wuthering Waves": "https://www.pcgamesn.com/wuthering-waves/codes",
    "Honkai Star Rail": "https://www.pcgamesn.com/honkai-star-rail/codes",
    "Zenless Zone Zero": "https://www.pcgamesn.com/zenless-zone-zero/codes"
}

items = []

for game, url in pages.items():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for li in soup.find_all("li"):
        strong = li.find("strong")
        if strong:
            code = strong.get_text(strip=True)
            reward = li.get_text(strip=True).replace(code, "").strip()
            items.append({
                "title": f"{code} ({game})",
                "description": reward,
                "link": url
            })

rss_items = "\n".join([
    f"""<item>
<title>{item['title']}</title>
<description><![CDATA[{item['description']}]]></description>
<link>{item['link']}</link>
</item>"""
    for item in items
])

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<title>Game Codes Feed</title>
<link>https://github.com/travian611-rgb/game-codes-rss</link>
<description>Automatically updated game codes</description>
<lastBuildDate>{datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')}</lastBuildDate>
{rss_items}
</channel>
</rss>
"""

with open("codes.xml", "w", encoding="utf-8") as f:
    f.write(rss)
