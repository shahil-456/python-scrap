from playwright.sync_api import sync_playwright
import time
import json
import os

mp4_url = None

save_file = "saves.json"

main_url = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=4f%2fOexzNsorKAF1lCFotvA%3d%3d"


url = None

pdf_url = None
current_name=None


def handle_request(request):
    global mp4_url
    global pdf_url

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
                # video["saved"] = True

            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("Saved:", video["name"])

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
                pdf["link"] = pdf_url
                # pdf["saved"] = True

            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print("Saved:", pdf["name"])


def process_videos(page):
    global current_name
    time.sleep(2)

    # with sync_playwright() as p:
        
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

            thumbnail.click()

            page.wait_for_timeout(3000)
            time.sleep(1)

            
            # Wait 2 seconds
            page.wait_for_timeout(3000)

            # Close video
            close_button = page.locator(
                "a.fancybox-close[title='Close']"
            )

            if close_button.is_visible():
                close_button.click()

        
            print("Saved:", name)


        except Exception as e:
            print(f"Skipped PDF {i}: {e}")
            continue

        
    # browser.close()



def process_pdfs(page):
    global current_name
    time.sleep(2)

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

        try:
            
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

        except Exception as e:
            print(f"Skipped PDF {i}: {e}")
            continue            





with sync_playwright() as p:
    # global url

    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        storage_state="state.json"
    )

    page = context.new_page()
    # 1. Go to page
    page.goto(main_url)
    page.wait_for_load_state("networkidle")

    # 2. If login div exists, click Login and then go to URL again
    login = page.locator("div.divButtonLoginWrapper input[type='submit']").first

    if login.count() > 0 and login.is_visible():
        login.click()
        page.wait_for_load_state("networkidle")
        page.goto(main_url)
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        context.storage_state(path="state.json")

    # 3. Get all course URLs
    links = page.locator(
        "div.factor360LearningActivityCatalogItemContent a.factor360HyperlinkForCatalog"
    ).evaluate_all(
        """els => els.map(e => e.href).slice(0, 2)"""
    )



    # Open every URL in a new tab
    for link in links:
        new_page = context.new_page()
        new_page.goto(link)
        new_page.wait_for_load_state("networkidle")
        time.sleep(1)

        url=new_page.url

        process_videos(new_page)

        time.sleep(3)

        process_pdfs(new_page)

        new_page.close()

        print(new_page.url)