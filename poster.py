import requests
import os
from bs4 import BeautifulSoup
from html import unescape
import re
import json
import time
import random

url = "https://cdn2.ispringcloud.com/out/1622-rQbR3-XfLea-eAevy/result/index.mp4"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5",
    "Accept-Language": "en-US,en;q=0.5",
    "Range": "bytes=0-",
    "Referer": "https://pro.ispringcloud.com/",
}

# response = requests.get(url, headers=headers, stream=True)

# print(response.status_code)
# print(response.headers.get("Content-Type"))
# print(response.headers.get("Content-Range"))
# print(response.headers.get("Content-Length"))

# Read first chunk

session = requests.Session()
session.headers.update(headers)


def get_video_url(short_url):
    # Follow redirect
    r = session.get(short_url, allow_redirects=True,timeout=30)


    print(r.url)
    print(session.cookies.get_dict())

    soup = BeautifulSoup(r.text, "html.parser")

    inp = soup.find("input", id="videoHtml5PlayerCode")
    if not inp:
        return None

    html = unescape(inp["value"])

    m = re.search(r'src="([^"]+)"', html)
    return m.group(1) if m else None



def download_video(url, filename, headers):
    os.makedirs("posters", exist_ok=True)
    filepath = os.path.join("posters", filename)

    with session.get(url, stream=True, timeout=30) as r:

        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)

    print(f"Downloaded: {filepath}")


# download_video(url, "hello.mp4", headers)

# print("Done")


with open("poster.json", "r", encoding="utf-8") as f:
    posters = json.load(f)


allowed_ids = {
    "ED1670", "ED1693", "ED1698", "ED1705", "ED1706",
    "ED1717", "ED1719", "ED1721", "ED1776", "ED1823",
    "ED1845", "SC1029", "SC1541", "SC1571", "SC1619"
}

posters = [
    item for item in posters
    if not item["saved"] and item["id"] in allowed_ids
]

random.shuffle(posters)


for poster in posters:
    if poster["saved"]:
        continue

    print(f'Processing: {poster["title"]}')

    video_url = get_video_url(poster["url"])

    if video_url:
        print(video_url)
        download_video(video_url, f'{poster["title"]}.mp4', headers)
        poster["saved"] = True
        with open("poster.json", "w", encoding="utf-8") as f:
            json.dump(posters, f, indent=4, ensure_ascii=False)

        time.sleep(3)
    else:
        print("Video URL not found.")

with open("posters.json", "w", encoding="utf-8") as f:
    json.dump(posters, f, indent=4, ensure_ascii=False)



# open posters.json file, and pass loop each to 

#     video_url = get_video_url("https://ispri.ng/qRkl7")

#     if video_url:
#         print(video_url)
#         download_video(video_url, "test.mp4", headers)
#     else:
#         print("Video URL not found.")




# with name and url
# print(os.path.getsize("output11.mp4"))

# with open("output11.mp4", "rb") as f:
#     print(f.read(32))