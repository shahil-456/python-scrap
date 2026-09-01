from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()

    page.goto("https://www.docmeded.com/video/item/11222")

    input("Login manually, then press Enter here...")

    context.storage_state(path="state.json")

    print("state.json saved")
    browser.close()