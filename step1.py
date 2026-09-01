from playwright.sync_api import sync_playwright
import time
import json
import os
import requests
import re





def get_videos(page):
    videos = []

    rows = page.locator("tbody tr")

    for i in range(rows.count()):
        row = rows.nth(i)

        name = row.locator("td:nth-child(2) a").inner_text()
        link = row.locator("td.video-preview-cell a").get_attribute("href")
        time.sleep(0.3)
        videos.append({
            "name": name.strip(),
            "link": link
        })

        

    return videos


def save_json(videos, filename="videos.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=4, ensure_ascii=False)


# with sync_playwright() as p:
#     browser = p.firefox.launch(headless=False)

#     context = browser.new_context(
#         storage_state="state.json"
#     )

#     page = context.new_page()

#     page.goto("https://www.docmeded.com/video/list?category=0&VideoModel_page=2")

#     time.sleep(400)

#     # trs = page.locator("tr")

#     # for i in range(trs.count()):
#     #     trs.nth(i).click()
#     # videos = get_videos(page)
#     # save_json(videos)
#     browser.close()


# def download_videos(filename="videos.json"):
#     with open(filename, "r", encoding="utf-8") as f:
#         videos = json.load(f)

#     with sync_playwright() as p:
#         browser = p.firefox.launch(headless=False)
#         context = browser.new_context(storage_state="state.json")
#         page = context.new_page()

#         for video in videos:
#             m3u8_url = None

#             def handle_request(request):
#                 nonlocal m3u8_url
#                 if ".m3u8" in request.url:
#                     m3u8_url = request.url

#             page.on("request", handle_request)

#             page.goto(video["link"])
#             page.wait_for_timeout(5000)

#             print(video["name"])
#             print(m3u8_url)

#         browser.close()




def download_videos(filename="videos.json"):
    with open(filename, "r", encoding="utf-8") as f:
        videos = json.load(f)

    # videos = videos[0]

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()

        for video in videos:
            ts_urls = []
            time.sleep(2)
            ts_saved = False

            def handle_request(request):

                if ".m3u8" in request.url:
                    print("M3U8:", request.url)

                if ".key" in request.url:
                    print("KEy:", request.url)

                if ".ts" in request.url:
                    ts_urls.append(request.url)
                    print("TS:", request.url)


            def save_1080_m3u8(request):
                if ".m3u8" not in request.url:
                    return

                url = request.url.replace("/720.m3u8", "/1080.m3u8")
                url = url.replace("/480.m3u8", "/1080.m3u8")

                safe_name = re.sub(r'[<>:"/\\|?*]', '', video["name"])
                folder = os.path.join("videos", safe_name)
                os.makedirs(folder, exist_ok=True)

                response = requests.get(url)

                if response.ok:
                    with open(os.path.join(folder, "1080.m3u8"), "w", encoding="utf-8") as f:
                        f.write(response.text)

                    print("Saved:", url)



            def save_1080_key(request):
                if ".key" not in request.url:
                    return

                url = request.url.replace("/720.key", "/1080.key")
                url = url.replace("/480.key", "/1080.key")

                safe_name = re.sub(r'[<>:"/\\|?*]', '', video["name"])
                folder = os.path.join("videos", safe_name)
                os.makedirs(folder, exist_ok=True)

                response = requests.get(url)

                if response.ok:
                    with open(os.path.join(folder, "1080.key"), "wb") as f:
                        f.write(response.content)

                    print("Saved key:", url)

            def save_1080_ts(request):
                nonlocal ts_saved
                if ".ts" not in request.url or ts_saved:
                    return

                url = request.url.replace("/720_", "/1080_")
                url = url.replace("/480_", "/1080_")

                safe_name = re.sub(r'[<>:"/\\|?*]', '', video["name"])
                folder = os.path.join("videos", safe_name)
                os.makedirs(folder, exist_ok=True)

                ts_name = url.split("/")[-1].split("?")[0]

                response = requests.get(url)

                if response.ok:
                    with open(os.path.join(folder, ts_name), "wb") as f:
                        f.write(response.content)

                    with open(os.path.join(folder, "ts.json"), "w", encoding="utf-8") as f:
                        json.dump({
                            "name": ts_name,
                            "link": url
                        }, f, indent=4)

                    print("Saved TS:", ts_name)

                ts_saved = True

                # raise StopIteration

            page.goto("https://www.docmeded.com/video/list?category=0")

            if ts_urls:
                continue

            video_page = context.new_page()

            video_page.on("request", handle_request)
            video_page.on("request", save_1080_m3u8)
            video_page.on("request", save_1080_key)
            video_page.on("request", save_1080_ts)

            video_page.goto(
                video["link"],
                referer="https://www.docmeded.com/video/list?category=0"
            )

            video_page.wait_for_timeout(10000)

            video_page.remove_listener("request", handle_request)
            video_page.close()

        browser.close()


download_videos()