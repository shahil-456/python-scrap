from playwright.sync_api import sync_playwright
import time
import json
import os

mp4_url = None

save_file = "full.json"

main_url = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=4f%2fOexzNsorKAF1lCFotvA%3d%3d"


url = None

key_name = None

pdf_url = None
current_name=None


def save_video_if_not_found(key_name, name):
    with open("full.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for site in data["sites"]:
        if site["key_name"] == key_name:
            for video in site.get("videos", []):
                if video["name"] == name:
                    return

            site["videos"].append({
                "name": name,
                "saved": False
            })

            with open("full.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return







def handle_request(request):
    global mp4_url
    global pdf_url

    print('three')

    if ".mp4" in request.url:
        # print("MP4 REQUEST:", request.url)
        mp4_url = request.url

        print('22222222')

        print(current_name)

        # with open(save_file, "r", encoding="utf-8") as f:
        #     data = json.load(f)

        #     site = next(
        #         s for s in data["sites"]
        #         if s["key_name"] == key_name
        #     )

        #     video = next(
        #         (v for v in site["videos"] if v["name"] == current_name),
        #         None
        #     )

        #     if video:
        #         video["link"] = mp4_url
        #         # video["saved"] = True

        #     with open(save_file, "w", encoding="utf-8") as f:
        #         json.dump(data, f, indent=4, ensure_ascii=False)

        #     print("Saved:", video["name"])

    if ".pdf" in request.url:
        # print("MP4 REQUEST:", request.url)
        pdf_url = request.url

        print('2')

        print(current_name)

        with open(save_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            site = next(
                s for s in data["sites"]
                if s["key_name"] == key_name
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
    global key_name

    time.sleep(1)

    # with sync_playwright() as p:
    with open("full.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    count_saved_vids = 0
    name_array=[]

    for site in data["sites"]:
        if site["key_name"] == key_name:
            count_saved_vids = len(site.get("videos", []))
            name_array = [video["name"] for video in site.get("videos", [])]
            break


    print(count_saved_vids)

        # Get all video names
    names = page.locator(
        "span[id*='lblAssetWithFileActivityName']"
    ).all_inner_texts()

    count_vids = len(names)

    print('key')
    print(key_name)

    if count_saved_vids >= count_vids:
        return

    #------------------------

    for name1 in names:
        save_video_if_not_found(key_name, name1)

    # Load saves.json
    # if os.path.exists(save_file):
    #     with open(save_file, "r", encoding="utf-8") as f:
    #         data = json.load(f)
    # else:
    #     data = {"sites": []}

    # # Find current URL
    # site = next(
    #     (s for s in data["sites"] if s["url"] == url),
    #     None
    # )

    # # Add URL if it doesn't exist
    # if site is None:
    #     site = {
    #         "url": url,
    #         "videos": []
    #     }
    #     data["sites"].append(site)

    # # Add missing video names
    # existing_names = {v["name"] for v in site["videos"]}

    # for name in names:
    #     name = name.strip()

    #     if name not in existing_names:
    #         site["videos"].append({
    #             "name": name,
    #             "saved": False
    #         })

    # # Save immediately
    # with open(save_file, "w", encoding="utf-8") as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)

    # Get count
    count = page.locator(
        "a.customActivityAssetLinkButton"
    ).count()

    print('two')

    time.sleep(1)
    page.on("request", handle_request)

    for i in range(count):
        print('for')

        try:
            print(f"[{i}] thumbnail locator")

            thumbnail = page.locator(
                "a.customActivityAssetLinkButton"
            ).nth(i)

            print(f"[{i}] thumbnail OK")

            time.sleep(1)
            name = page.locator(
                "span[id*='lblAssetWithFileActivityName']"
            ).nth(i).inner_text().strip()

            
            if name in name_array:
                continue

            current_name=name

            print(current_name)



            print(f"[{i}] name locator")



            print(f"[{i}] name OK: {name}")

            current_name = name
            print(f"[{i}] clicking thumbnail")

            thumbnail.click()

            print(f"[{i}] thumbnail clicked")

            page.wait_for_timeout(3000)
            time.sleep(2)

            print(f"[{i}] close button locator")

            close_button = page.locator(
                "a.fancybox-close[title='Close']"
            )

            print(f"[{i}] checking close button")

            if close_button.is_visible():
                print(f"[{i}] close button visible, clicking")
                close_button.click()
                print(f"[{i}] close button clicked")
            else:
                print(f"[{i}] close button not visible")

            print(f"[{i}] Saved: {name}")

        except Exception as e:
            print(f"[{i}] ERROR: {type(e).__name__}: {e}")
            continue



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
            "key_name": key_name,
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

        key_name = new_page.locator(
            "#MainContent_MainContent_MainContent_ucUserLearningActivityDashboardForLearner_lblLearningActivityDisplayName"
        ).inner_text()

        print(key_name)

        process_videos(new_page)

        time.sleep(3)

        # process_pdfs(new_page)

        # new_page.close()

        print(new_page.url)