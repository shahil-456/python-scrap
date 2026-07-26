import requests
import os
import re
import json
import time


def clean_name(name):
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    return name.strip(" .")


def download_video(url, folder):
    r = requests.get(url, stream=True, timeout=1000)
    r.raise_for_status()

    filename = url.split("filename=")[1].split("&")[0].replace("+", " ")
    filename = clean_name(filename)


    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, filename + ".mp4")

    
    with open(filepath, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

    print("Saved:", filepath)


with open("links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

for item in links:

    if item.get("saved", False):
        continue

    try:
        folder = os.path.join(
            *[clean_name(x) for x in item["breadcrumb"]]
        )

        download_video(
            item["url"],
            folder
        )

        item["saved"] = True

        with open("links.json", "w", encoding="utf-8") as f:
            json.dump(links, f, indent=2)

        time.sleep(2)

    except Exception as e:
        print("Error:", e)