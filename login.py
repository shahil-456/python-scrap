from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://education.asnc.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=9ei2i1utfAQiVfCcsAIhrg%3D%3D")

    input("Login manually, then press Enter here...")

    context.storage_state(path="state.json")

    print("state.json saved")
    browser.close()