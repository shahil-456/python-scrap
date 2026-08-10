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


with open("full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

errors = 0

with open("errors.txt", "a", encoding="utf-8") as err_file:

    for site in data["sites"]:

        location = clean_name(site["location"])

        for video in site.get("videos", []):

            if video.get("saved", False):
                continue

            try:
                folder = os.path.join(
                    "my courses",
                    location,
                    clean_name(video["name"])
                )

                download_file(
                    video["link"],
                    folder,
                    video["name"],
                    ".mp4"
                )

                video["saved"] = True

                with open("full.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                time.sleep(2)

            except Exception as e:
                errors += 1
                print("Error:", e)

                # err_file.write(
                #     f"{video['link']}\n{e}\n\n"
                # )

        for pdf in site.get("pdfs", []):

            if pdf.get("saved", False):
                continue

            try:
                folder = os.path.join(
                    "my courses",
                    location,
                    clean_name(pdf["name"])
                )

                download_file(
                    pdf["link"],
                    folder,
                    pdf["name"],
                    ".pdf"
                )

                pdf["saved"] = True

                with open("full.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                time.sleep(2.3)

            except Exception as e:
                errors += 1
                print("Error:", e)

                # err_file.write(
                #     f"{pdf['link']}\n{e}\n\n"
                # )

print(f"\nCompleted")
print(f"Downloaded: {downloaded}")
print(f"Errors: {errors}")