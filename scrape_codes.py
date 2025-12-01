import requests
import json
from bs4 import BeautifulSoup
import datetime

pages = {
    "Wuthering Waves": "https://www.pcgamesn.com/wuthering-waves/codes",
    "Honkai Star Rail": "https://www.pcgamesn.com/honkai-star-rail/codes",
    "Zenless Zone Zero": "https://www.pcgamesn.com/zenless-zone-zero/codes"
}

items = []

for game, url in pages.items():
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    # Extract the embedded JSON
    script = soup.find("script", {"id": "__NEXT_DATA__"})
    if not script:
        continue

    data = json.loads(script.string)

    # PCGamesN puts the article content under this path
    try:
        codes = data["props"]["pageProps"]["article"]["blocks"]
    except KeyError:
        continue

    # Find any blocks that contain code lists
    for block in codes:
        if block.get("__typename") == "ListBlock":
            for entry in block.get("items", []):
                # Must contain a bold code item
                code = None
                reward = None
                for child in entry.get("children", []):
                    if child.get("tag") == "strong":
                        code = child.get("children", [""])[0]
                    else:
                        # Other children contain reward text
                        text = "".join(child.get("children", []))
                        if text and "Expires" not in text:
                            reward = text.strip()

                if code:
                    items.append({
                        "title": f"{code} ({game})",
                        "description": reward or "",
                        "link": url
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
