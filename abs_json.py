from bs4 import BeautifulSoup
import json

def clean_name(name):
    return name.strip()

with open("abs.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

data = []

for tr in soup.find_all("tr"):
    title = tr.select_one("div.title a")
    if not title:
        continue

    url = title["href"]
    print(url)

    data.append({
        "id": title["href"].split("FID=")[-1],
        "title": clean_name(title.get_text(strip=True)),
        "url": "https://apps.arrs.org" + title["href"],
        "saved": False
    })

with open("abs.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Saved {len(data)} records.")