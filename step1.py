import os
from playwright.sync_api import sync_playwright
import time
import json

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


def get_courses(page):
    items = []

    names = page.locator("a.learningActivityTitleForMultiLevelDisplay")

    for i in range(names.count()):
        name = names.nth(i).inner_text().strip()

        parent = names.nth(i).locator(
            "xpath=ancestor::div[contains(@class,'factor360MultiLevelChildLearningActivityLayout_Title')]"
        )

        access_links = parent.locator(
            "xpath=following-sibling::div[contains(@class,'factor360MultiLevelChildLearningActivityLayout_childList')]//a[contains(@class,'button')]"
        )

        for j in range(access_links.count()):
            items.append({
                "name": name,
                "access_url": access_links.nth(j).get_attribute("href")
            })

    return items


def save_json(main_url, items):
    data = {
        "main_url": main_url,
        "items": items
    }

    with open("courses.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    main_url = "https://education.asnc.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=9ei2i1utfAQiVfCcsAIhrg%3D%3D"

    p, browser, page = open_browser()

    try:
        get_page(page, main_url)

        items = get_courses(page)
        save_json(main_url, items)

        print(f"Saved {len(items)} items")

    finally:
        browser.close()
        p.stop()


if __name__ == "__main__":
    main()









def process_urls(page, items):
    for item in items:
        tab = page.context.new_page()

        tab.goto(item["access_url"])
        tab.wait_for_load_state("networkidle")

        first_div = tab.locator(
            "div[class='flex: 0 1 auto;'] a.factor360Hyperlink"
        ).first

        name = first_div.inner_text().strip()

        item["page_name"] = name

        # Click first div
        first_div.click()
        tab.wait_for_load_state("networkidle")

        # Close tab
        tab.close()





def save_json(main_url, items):
    data = {
        "main_url": main_url,
        "items": items
    }

    with open("courses.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)





# def open_browser(p):
#     state_file = "state.json"
#     login_url = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=hWBfF0h8FfilW%2fkGSfJqIw%3d%3d"

#     browser = p.firefox.launch(
#         headless=False
#     )

#     if os.path.exists(state_file):
#         context = browser.new_context(
#             storage_state=state_file,
#             accept_downloads=True,
#             viewport=None,
#             locale="en-US",
#             timezone_id="Asia/Kolkata",
#             user_agent=(
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/142.0.0.0 Safari/537.36"
#             ),
#             extra_http_headers={
#                 "Accept-Language": "en-US,en;q=0.9"
#             }
#         )

#     else:
#         context = browser.new_context(
#             accept_downloads=True,
#             viewport=None,
#             locale="en-US",
#             timezone_id="Asia/Kolkata",
#             user_agent=(
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                 "AppleWebKit/537.36 (KHTML, like Gecko) "
#                 "Chrome/142.0.0.0 Safari/537.36"
#             ),
#             extra_http_headers={
#                 "Accept-Language": "en-US,en;q=0.9"
#             }
#         )

#         page = context.new_page()

#         page.goto(
#             login_url,
#             wait_until="domcontentloaded"
#         )

#         input("Login manually, then press ENTER...")

#         context.storage_state(path=state_file)
#         print("Session saved.")

#     return browser, context


# def handle_response(response):
# # print(response.url)
#     if "PdfPages/SecurePdfHandler" in response.url:
#         print("PDF response:", response.url)

#         try:
#             body = response.body()

#             with open("save.pdf", "wb") as f:
#                 f.write(body)

#             print("PDF saved")

#         except Exception as e:
#             print("PDF error:", e)

# def handle_request(request):
#     # print(request.url)
#     if "PdfPages/SecurePdfHandler" in request.url:
#         print("PDF request:", request.url)

#         try:
#             body = request.body()

#             with open("save.pdf", "wb") as f:
#                 f.write(body)

#             print("PDF saved")

#         except Exception as e:
#             print("PDF error:", e)
            
#     page.on("request", handle_request)

# with sync_playwright() as p:

#     browser, context = open_browser(p)

#     page = context.new_page()


#     page.on("response", handle_response)
#     page.on("response", handle_response)


#     page.goto(
#         "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=4f%2FOexzNsorKAF1lCFotvA%3D%3D",
#         wait_until="domcontentloaded"
#     )

#     # input("Press ENTER to exit...")
#     time.sleep(1000)
#     # browser.close()

# import json
# from playwright.sync_api import sync_playwright


# def open_browser():
#     p = sync_playwright().start()
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context(storage_state="state.json")
#     page = context.new_page()
#     return p, browser, page


# def get_page(page, url):
#     page.goto(url)
#     page.wait_for_load_state("networkidle")


# def get_courses(page):
#     items = []

#     names = page.locator("a.learningActivityTitleForMultiLevelDisplay")

#     for i in range(names.count()):
#         name = names.nth(i).inner_text().strip()

#         parent = names.nth(i).locator(
#             "xpath=ancestor::div[contains(@class,'factor360MultiLevelChildLearningActivityLayout_Title')]"
#         )

#         access_links = parent.locator(
#             "xpath=following-sibling::div[contains(@class,'factor360MultiLevelChildLearningActivityLayout_childList')]//a[contains(@class,'button')]"
#         )

#         for j in range(access_links.count()):
#             items.append({
#                 "name": name,
#                 "access_url": access_links.nth(j).get_attribute("href")
#             })

#     return items


# def save_json(main_url, items):
#     data = {
#         "main_url": main_url,
#         "items": items
#     }

#     with open("courses.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)


# def main():
#     main_url = "https://education.asnc.org/your-main-url"

#     p, browser, page = open_browser()

#     try:
#         get_page(page, main_url)

#         items = get_courses(page)
#         save_json(main_url, items)

#         print(f"Saved {len(items)} items")

#     finally:
#         browser.close()
#         p.stop()


# if __name__ == "__main__":
#     main()