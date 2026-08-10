import json
import os
from playwright.sync_api import sync_playwright
import time


pdf_url = None

save_file = "saves.json"
url = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=hWBfF0h8FfilW%2fkGSfJqIw%3d%3d"


pdf_url = None
current_name=None

def handle_request(request):
    global pdf_url

    if ".pdf" in request.url:
        # print("MP4 REQUEST:", request.url)
        pdf_url = request.url

        print('2')

        print(current_name)

        with open(save_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            site = next(
                s for s in data["sites"]
                if s["url"] == url
            )

            pdf = next(
                (v for v in site["pdfs"] if v["name"] == current_name),
                None
            )

            if pdf:
                pdf["pdf"] = pdf_url
                pdf["saved"] = True

            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("Saved:", pdf["name"])

def process_pdfs():
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

        # Get all pdf names

        names = page.locator(
            "span[id*='spanSingleLearningActivityAsset']"
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
                "pdfs": []
            }
            data["sites"].append(site)

        # Add missing pdf names
        existing_names = {v["name"] for v in site["pdfs"]}

        for name in names:
            name = name.strip()

            if name not in existing_names:
                site["pdfs"].append({
                    "name": name,
                    "saved": False
                })

        # Save immediately
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # Get count
        count = page.locator(
            "a.factor360NoDecorationHyperlink"
        ).count()

        # print(count)

        time.sleep(1)
        page.on("request", handle_request)

        for i in range(count):

            thumbnail = page.locator(
                "a.factor360NoDecorationHyperlink"
            ).nth(i)

            time.sleep(1)

            name = page.locator(
                "span[id*='spanSingleLearningActivityAsset']"
            ).nth(i).inner_text().strip()

            current_name=name

            print(current_name)

            thumbnail.click()

            page.wait_for_timeout(3000)
            time.sleep(1)


            # Wait 2 seconds
            page.wait_for_timeout(3000)

            # Close pdf
            close_button = page.locator(
                "a.fancybox-close[title='Close']"
            )

            if close_button.is_visible():
                close_button.click()

        
            print("Saved:", name)

        browser.close()


process_pdfs()