from playwright.sync_api import sync_playwright


def process_links():
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

        page.goto(
            "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=4f%2FOexzNsorKAF1lCFotvA%3D%3D",
            wait_until="domcontentloaded"
        )

        links = page.locator("a.factor360HyperlinkForCatalog").all()

        for link in links:
            url = link.get_attribute("href")

            if not url:
                continue

            tab = context.new_page()

            tab.goto(
                url,
                wait_until="domcontentloaded"
            )

            print("Opened:", url)

            page.wait_for_timeout(120000)
            time.sleep(10)

            tab.close()

        browser.close()



process_links()