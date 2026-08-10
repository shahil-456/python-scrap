from playwright.sync_api import sync_playwright
import time

url = "https://learningcenter.hfsa.org/Users/SelectedExamQuizStatus.aspx?UserExamQuizID=keECVoz4TsS1zHE64HLubA%3d%3d"


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        storage_state="state.json",
        accept_downloads=True
    )

    page = context.new_page()
    page.goto(url, wait_until="networkidle")

    time.sleep(2)

    # Click first question only
    page.locator(
        "div.factor360QuestionBox"
    ).nth(0).locator(
        "a.factor360UserQuestionLinkButton"
    ).click()

    page.wait_for_load_state("networkidle")

    time.sleep(2)

    i = 1

    while True:

        # Save PDF
        page.pdf(
            path=f"qbank/question_{i}.pdf",
            format="A4",
            print_background=True
        )

        print(f"Saved question_{i}.pdf")

        # Next question
        next_btn = page.locator(
            "a#MainContent_MainContent_MainContent_ucQuestionNavigation_lnkBtnNextQuestion"
        )

        if next_btn.count() == 0 or not next_btn.is_visible():
            print("No more questions.")
            break

        next_btn.click()

        page.wait_for_load_state("networkidle")

        time.sleep(3)

        i += 1

    browser.close()

    # browser.close()