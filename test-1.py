from playwright.sync_api import sync_playwright
import time

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()

#     page.goto("https://education.asnc.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=9ei2i1utfAQiVfCcsAIhrg%3D%3D")

#     input("Login manually, then press Enter here...")

#     # context.storage_state(path="state.json")

#     print("state.json saved")
#     browser.close()

def handle_request(request):
    global mp4_url
    global pdf_url

    # print('three')

    if ".mp4" in request.url:
        # print("MP4 REQUEST:", request.url)
        mp4_url = request.url

        print(mp4_url)

        # with open(save_file, "r", encoding="utf-8") as f:
        #     data = json.load(f)

        #     site = next(
        #         (s for s in data["sites"] if s["key_name"] == key_name),
        #         None
        #     )

        #     if site is None:
        #         return

        #     video = next(
        #         (v for v in site["videos"] if v["name"] == current_name),
        #         None
        #     )

        #     if video:
        #         video["link"] = mp4_url
        #         # video["saved"] = True

        #     with open(save_file, "w", encoding="utf-8") as f:
        #         json.dump(data, f, indent=4, ensure_ascii=False)

        #     if video:
        #         print("Saved:", video["name"])

    if ".pdf" in request.url:
        
        pdf_url = request.url
        print(pdf_url)

        # with open(save_file, "r", encoding="utf-8") as f:
        #     data = json.load(f)

        #     site = next(
        #         (s for s in data["sites"] if s["key_name"] == key_name),
        #         None
        #     )

        #     if site is None:
        #         return

        #     pdf = next(
        #         (v for v in site["pdfs"] if v["name"] == current_name),
        #         None
        #     )

        #     if pdf:
        #         pdf["link"] = pdf_url
        #         # pdf["saved"] = True

        #     with open(save_file, "w", encoding="utf-8") as f:
        #         json.dump(data, f, indent=4, ensure_ascii=False)

        #     if pdf:
        #         print("Saved:", pdf["name"])


def process_pdfs(page):
    pdfs = page.locator("a:has(i.file.pdf.icon)")

    for i in range(pdfs.count()):
        pdfs = page.locator("a:has(i.file.pdf.icon)")
        pdfs.nth(i).click()

        page.wait_for_timeout(2000)

        frame = page.locator("iframe.fancybox-iframe").content_frame

        display_btn = frame.locator(
            'input#ctl00_BodyContent_rlvLearningActivityAssetList_ctrl0_btnViewLearningActivityAsset'
        )

        display_btn.wait_for(state="visible", timeout=5000)
        display_btn.click()

        time.sleep(1)

        page.wait_for_timeout(2000)

        page.locator(
            'a.fancybox-item.fancybox-close[title="Close"]'
        ).click()

        page.wait_for_timeout(500)

STATE_FILE = "state.json"
LOGIN_URL = "https://education.asnc.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=9ei2i1utfAQiVfCcsAIhrg%3D%3D"



def open_browser():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    return p, browser, page

def get_page(page, url):
    page.goto(url)
    page.wait_for_load_state("networkidle")


def process_videos(page):
    videos = page.locator(
        "span.activityAssetCustomClassForReadMore"
    )

    count = videos.count()
    print("Videos:", count)

    # for i in range(count):
    #     videos = page.locator(
    #         "span.activityAssetCustomClassForReadMore"
    #     )

    #     name = videos.nth(i).inner_text().strip()
    #     print(name)


    # videos = page.locator("div.learningActivityAssetTitleContainerParent")

    count = videos.count()

    for i in range(count):
        name = videos.nth(i).locator(
            "div[id*='pnlActivityAssetTitle'] span"
        ).inner_text().strip()

        print(name)    

        # Click thumbnail
        videos.nth(i).click()

        # Wait for page/modal
        page.wait_for_timeout(4000)

        # Close
        close_btn = page.locator(
            'a.fancybox-item.fancybox-close[title="Close"]'
        )
        time.sleep(1)
        if close_btn.count() > 0:
            close_btn.first.click()

        page.wait_for_timeout(1000)




def main():
    main_url = "https://education.asnc.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=9ei2i1utfAQiVfCcsAIhrg%3D%3D"


    url="https://education.asnc.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=bmCtOOt5fQz5%2bmG4SQ3u%2bA%3d%3d&OriginatedFromUserLearningActivityID=4ntI%2bo6h%2byooptsrngM0Kg%3d%3d"

    page="2026 Board Prep Session I: Pre-recorded Lectures"

    p, browser, page = open_browser()
    page.on("request", handle_request)

    try:
        get_page(page, url)

        # process_videos(page)
        # process_pdfs(page)


        time.sleep(1000)

        # print(f"Saved {len(items)} items")

    finally:
        browser.close()
        p.stop()


if __name__ == "__main__":
    main()