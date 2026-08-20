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

data = {
    "datas": []
}

mp4_url = None

url = None

key_name = None
file_name = None

pdf_url = None
current_name=None



def handle_request(request):
    global mp4_url
    global pdf_url
    global data

    # print('three')

    if ".mp4" in request.url or ".mov" in request.url:
        for item in data["datas"]:
            if not item["video"]:
                item["video"] = request.url
                break
        
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
        if any(item["pdf"] == request.url for item in data["datas"]):
            return

        for item in data["datas"]:
            if not item["pdf"]:
                item["pdf"] = request.url
                break

        print(request.url)

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
    global file_name


    for i in range(pdfs.count()):
        pdfs = page.locator("a:has(i.file.pdf.icon)")
        pdfs.nth(i).click()
        # file_name=name

        page.wait_for_timeout(3000)

        frame = page.locator("iframe.fancybox-iframe").content_frame

        display_btn = frame.locator(
            'input#ctl00_BodyContent_rlvLearningActivityAssetList_ctrl0_btnViewLearningActivityAsset'
        )

        display_btn.wait_for(state="visible", timeout=4000)
        display_btn.click()

        time.sleep(1)

        page.wait_for_timeout(2000)

        page.locator(
            'a.fancybox-item.fancybox-close[title="Close"]'
        ).click()

        page.wait_for_timeout(700)

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
    global data
    global file_name

    count = videos.count()
    print("Videos:", count)
    # data["datas"] = []
    # for i in range(count):
    #     videos = page.locator(
    #         "span.activityAssetCustomClassForReadMore"
    #     )

    #     name = videos.nth(i).inner_text().strip()
    #     print(name)

    # videos = page.locator("div.learningActivityAssetTitleContainerParent")

    count = videos.count()

    for i in range(count):
        # name = videos.nth(i).locator(
        #     "div[id*='pnlActivityAssetTitle'] span"
        # ).inner_text().strip()
        name = videos.nth(i).locator("xpath=..").inner_text().strip()

        data["datas"].append({
            "name": name,
            "video": "",
            "pdf": "",
            "saved": False
        })
        file_name=name
        print(file_name)
        # Click thumbnail
        videos.nth(i).click()
        time.sleep(1)
        # Wait for page/modal
        page.wait_for_timeout(5000)

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


    url="https://education.asnc.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=I8ii40xpRMlVXQxiIIOQLQ%3d%3d"

    page="2026 Board Prep Session III: Pre-recorded Lectures"

    p, browser, page = open_browser()
    page.on("request", handle_request)

    try:
        get_page(page, url)

        process_videos(page)
        process_pdfs(page)
        print(data)

        time.sleep(1000)

        # print(f"Saved {len(items)} items")

    finally:
        browser.close()
        p.stop()


if __name__ == "__main__":
    main()