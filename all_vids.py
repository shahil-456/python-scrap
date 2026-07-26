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

total = len(links)
downloaded = 0
errors = 0

with open("errors.txt", "a", encoding="utf-8") as err_file:

    for index, item in enumerate(links, start=1):

        if item.get("saved", False):
            continue

        print(f"[{index}/{total}] Downloading...")

        try:
            folder = os.path.join(
                *[clean_name(x) for x in item["breadcrumb"]]
            )

            download_video(
                item["url"],
                folder
            )

            item["saved"] = True
            downloaded += 1

            with open("links.json", "w", encoding="utf-8") as f:
                json.dump(links, f, indent=2)

            print(f"Downloaded: {downloaded}")

            time.sleep(2)

        except Exception as e:
            errors += 1

            print(f"Error: {e}")

            err_file.write(
                f"{item['url']}\n{e}\n\n"
            )

print(f"\nCompleted")
print(f"Downloaded: {downloaded}")
print(f"Errors: {errors}")