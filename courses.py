import requests
import os
import re
import json
import time


def clean_name(name):
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    return name.strip(" .")


def download_file(url, folder, filename, extension):
    r = requests.get(url, stream=True, timeout=3000)
    r.raise_for_status()

    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(
        folder,
        clean_name(filename) + extension
    )

    with open(filepath, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

    print("Saved:", filepath)


with open("courses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

errors = 0
downloaded = 0

for item in data["items"]:

    course_name = clean_name(item["name"])
    page = item["page"]

    page_folder = os.path.join(
        "my courses",
        course_name,
        clean_name(page["name"])
    )

    for video in page["datas"]:

        if video.get("saved", False):
            continue

        try:

            video_folder = os.path.join(
                page_folder,
                clean_name(video["name"])
            )

            download_file(video["video"], video_folder, video["name"], ".mp4")


            download_file(video["pdf"], video_folder, video["name"], ".pdf")

            video["saved"] = True
            downloaded += 1

            with open("courses.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            time.sleep(2)

        except Exception as e:
            errors += 1
            print("Error:", e)

print("\nCompleted")
print("Downloaded:", downloaded)
print("Errors:", errors)