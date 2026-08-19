from playwright.sync_api import sync_playwright
import os
import re
import requests
from urllib.parse import urljoin, urlparse
import time

MAIN_URL = "https://learningcenter.hfsa.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=xGXMIoOQlNbCttrPAlerhg%3d%3d"


def open_browser(p):
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        storage_state="state.json"
    )

    return browser, context


def open_main_page(context):
    page = context.new_page()

    page.goto(
        MAIN_URL,
        wait_until="domcontentloaded"
    )

    return page




def open_exam_page(page):
    page.wait_for_load_state("networkidle")

    link = page.locator(
        "a#MainContent_MainContent_MainContent_ucUserLearningActivityDashboardForLearner_ucUserLearningActivity_MyCourseDetail_hlPostExamAction"
    )

    url = "https://learningcenter.hfsa.org/Users/" + link.get_attribute("href").replace("../", "")

    print(url)

    if url:
        # url = page.url.rsplit("/", 1)[0] + "/" + url.lstrip("../")
        page.goto(url, wait_until="domcontentloaded")

    return page




def click_first_question(page):
    page.locator(
        "a.factor360UserQuestionLinkButton"
    ).first.click()
    time.sleep(2)



i=1

def click_next_question(page):
    page.locator(
        "a#MainContent_MainContent_MainContent_ucQuestionNavigation_lnkBtnNextQuestion"
    ).click()


def save_quiz_page(page):
    folder = "offline_quiz"
    global i

    os.makedirs(folder, exist_ok=True)

    html = page.content()

   

    with open(os.path.join(folder, f"quiz{i}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    # time.sleep(2)
    i += 1

    # click_next_question(page)
    print("Done")



with sync_playwright() as p:

    browser, context = open_browser(p)

    page = open_main_page(context)

    page = open_exam_page(page)

    # click_first_question(page)

    page.wait_for_load_state("networkidle")

    time.sleep(3)

    # page = open_exam_page(page)

    click_first_question(page)

    time.sleep(3)

    save_quiz_page(page)

    for i in range(1, 40):
        try:
            click_next_question(page)
            time.sleep(3)
            save_quiz_page(page)
            print(page.url)

        except Exception as e:
            print(f"[{i}] ERROR: {type(e).__name__}: {e}")
            time.sleep(3)
            continue

        # input("Press ENTER to exit...")



























