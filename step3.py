import json
import os
from playwright.sync_api import sync_playwright
import time


mp4_url = None

save_file = "saves.json"
url = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=hWBfF0h8FfilW%2fkGSfJqIw%3d%3d"

# def handle_request(request):
#     global mp4_url

#     if ".mp4" in request.url:
#         print("MP4 REQUEST:", request.url)
#         mp4_url = request.url

mp4_url = None
current_name=None

def handle_request(request):
    global mp4_url

    if ".mp4" in request.url:
        # print("MP4 REQUEST:", request.url)
        mp4_url = request.url

        print('2')

        print(current_name)

        with open(save_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            site = next(
                s for s in data["sites"]
                if s["url"] == url
            )

            video = next(
                (v for v in site["videos"] if v["name"] == current_name),
                None
            )

            if video:
                video["link"] = mp4_url
                video["saved"] = True

            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("Saved:", video["name"])

def process_videos():
    global current_name
    time.sleep(2)
    # url = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=hWBfF0h8FfilW%2fkGSfJqIw%3d%3d"
    # save_file = "saves.json"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ]
        )

        context = browser.new_context(
            storage_state="state.json",
            accept_downloads=True
        )

        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")

        # Get all video names
        names = page.locator(
            "span[id*='lblAssetWithFileActivityName']"
        ).all_inner_texts()

        # Load saves.json
        if os.path.exists(save_file):
            with open(save_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"sites": []}

        # Find current URL
        site = next(
            (s for s in data["sites"] if s["url"] == url),
            None
        )

        # Add URL if it doesn't exist
        if site is None:
            site = {
                "url": url,
                "videos": []
            }
            data["sites"].append(site)

        # Add missing video names
        existing_names = {v["name"] for v in site["videos"]}

        for name in names:
            name = name.strip()

            if name not in existing_names:
                site["videos"].append({
                    "name": name,
                    "saved": False
                })

        # Save immediately
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Get count
        count = page.locator(
            "a.customActivityAssetLinkButton"
        ).count()

        # print(count)

        time.sleep(1)
        page.on("request", handle_request)

        for i in range(count):

            try:
               thumbnail = page.locator(
                "a.customActivityAssetLinkButton"
                ).nth(i)

                time.sleep(1)

                name = page.locator(
                    "span[id*='lblAssetWithFileActivityName']"
                ).nth(i).inner_text().strip()

                current_name=name

                print(current_name)

                # with open(save_file, "r", encoding="utf-8") as f:
                #     data = json.load(f)

                # site = next(
                #     s for s in data["sites"]
                #     if s["url"] == url
                # )

                # video = next(
                #     (v for v in site["videos"] if v["name"] == name),
                #     None
                # )

                # if video and video["saved"]:
                #     print("Already saved:", name)
                #     continue

                # mp4_url = None

                thumbnail.click()

                page.wait_for_timeout(3000)
                time.sleep(1)

                # if mp4_url:
                #     for video in site["videos"]:
                #         if video["name"] == name:
                #             video["link"] = mp4_url
                #             video["saved"] = True
                #             break

                #     with open(save_file, "w", encoding="utf-8") as f:
                #         json.dump(data, f, indent=4, ensure_ascii=False)

                #     print("Saved:", name)


                # page.on("response", handle_response)

                # Wait 2 seconds
                page.wait_for_timeout(3000)

                # Close video
                close_button = page.locator(
                    "a.fancybox-close[title='Close']"
                )

                if close_button.is_visible():
                    close_button.click()

                # Mark as saved immediately
                # for video in site["videos"]:
                #     if video["name"] == name:
                #         video["saved"] = True
                #         break

                # with open(save_file, "w", encoding="utf-8") as f:
                #     json.dump(data, f, indent=4, ensure_ascii=False)

                print("Saved:", name)


            except Exception as e:
                print(f"Skipped PDF {i}: {e}")
                continue

            
        browser.close()


process_videos()