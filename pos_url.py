from bs4 import BeautifulSoup
import json
import re

with open("poster.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

data = []

def clean_name(name):
        return re.sub(r'[<>:"/\\|?*]', '', name)

for a in soup.select('a.video[data-video]'):
    data.append({
        "id": a.get("fid"),
        "title": clean_name(a.get_text(strip=True)),
        "url": a["data-video"],
        "saved": False
    })

with open("poster.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Saved {len(data)} records.")