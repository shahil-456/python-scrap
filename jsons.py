from bs4 import BeautifulSoup
import json
import re

with open("session.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

urls = []

for tr in soup.find_all("tr"):

    link = tr.find("a", class_="session-button")

    if not link:
        continue

    container = tr.find("div", class_="ac-container")

    if not container:
        continue

    label = container.find("label")

    if not label:
        continue

    def clean_name(name):
        return re.sub(r'[<>:"/\\|?*]', '', name)


    urls.append({
        "id": len(urls) + 1,
        "name": clean_name(label.get_text(strip=True)),
        "url": link["href"],
        "saved": False
    })

with open("urls.json", "w", encoding="utf-8") as f:
    json.dump(urls, f, indent=4, ensure_ascii=False)

print("saved")