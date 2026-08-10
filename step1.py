import os
from playwright.sync_api import sync_playwright


STATE_FILE = "state.json"
LOGIN_URL = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=hWBfF0h8FfilW%2fkGSfJqIw%3d%3d"



def open_browser(p):
    state_file = "state.json"
    login_url = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=hWBfF0h8FfilW%2fkGSfJqIw%3d%3d"

    browser = p.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ]
    )

    if os.path.exists(state_file):
        context = browser.new_context(
            storage_state=state_file,
            accept_downloads=True,
            viewport=None,
            locale="en-US",
            timezone_id="Asia/Kolkata",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/142.0.0.0 Safari/537.36"
            ),
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9"
            }
        )

    else:
        context = browser.new_context(
            accept_downloads=True,
            viewport=None,
            locale="en-US",
            timezone_id="Asia/Kolkata",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/142.0.0.0 Safari/537.36"
            ),
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9"
            }
        )

        page = context.new_page()

        page.goto(
            login_url,
            wait_until="domcontentloaded"
        )

        input("Login manually, then press ENTER...")

        context.storage_state(path=state_file)
        print("Session saved.")

    return browser, context


with sync_playwright() as p:

    browser, context = open_browser(p)

    page = context.new_page()

    page.goto(
        "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=4f%2FOexzNsorKAF1lCFotvA%3D%3D",
        wait_until="domcontentloaded"
    )

    input("Press ENTER to exit...")

    browser.close()

# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.firefox.launch(headless=False)

#     context = browser.new_context()
#     page = context.new_page()

#     page.goto("https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=4f%2FOexzNsorKAF1lCFotvA%3D%3D")

#     input("Login in Firefox, then press ENTER...")

#     context.storage_state(path="state.json")

#     browser.close()