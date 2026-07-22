import json
import os
import re
from playwright.sync_api import sync_playwright
import time

TRACK_FILE = "clicked.json"

def load_clicked():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)

        if not isinstance(db, dict):
            db = {}



def save_clicked(data):
    with open(TRACK_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    if not isinstance(db, dict):
        db = {}




def click_all_in_new_tabs(context, page):
    TRACK_FILE = "clicked.json"

    page.wait_for_selector(
        "a[id*='lnkBtnLearningActivityTitle']",
        timeout=300000
    )

    current_url = page.url

    # Load JSON
    db = {}

    if os.path.exists(TRACK_FILE):
        try:
            with open(TRACK_FILE, "r", encoding="utf-8") as f:
                db = json.load(f)

            if not isinstance(db, dict):
                db = {}
        except:
            db = {}

    # First time: save all titles
    if current_url not in db:
        links = page.locator("a[id*='lnkBtnLearningActivityTitle']")

        db[current_url] = []

        for i in range(links.count()):
            db[current_url].append({
                "title": links.nth(i).inner_text().strip(),
                "saved": False
            })

        with open(TRACK_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2)

    while True:
        with open(TRACK_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)

        if not isinstance(db, dict):
            db = {}

        items = db.get(current_url, [])

        item = next((x for x in items if not x["saved"]), None)

        if item is None:
            print("All completed.")
            break

        tab = context.new_page()
        tab.set_default_timeout(300000)
        tab.set_default_navigation_timeout(300000)

        try:
            tab.goto(
                current_url,
                wait_until="domcontentloaded",
                timeout=300000
            )

            tab.wait_for_selector(
                "a[id*='lnkBtnLearningActivityTitle']",
                timeout=300000
            )

            tab.get_by_role(
                "link",
                name=item["title"],
                exact=True
            ).click(timeout=300000)

            time.sleep(5)

            tab.wait_for_load_state(
                "domcontentloaded",
                timeout=300000
            )

            print(tab.url)

            # Process detail page here

            item["saved"] = True
            db[current_url] = items

            with open(TRACK_FILE, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=2)

        finally:
            tab.close()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(storage_state="state.json")
    context.set_default_timeout(300000)
    context.set_default_navigation_timeout(300000)

    page = context.new_page()

    page.goto(
        "https://learning.aad.org/Users/LearningActivity/LearningActivityDetail.aspx?LearningActivityID=qMOha6AJQxDZq9uPUx0xUQ%3d%3d&OriginatedFromUserLearningActivityID=ckFyCLAsgnfVymqDAzEatA%3d%3d",
        wait_until="domcontentloaded",
        timeout=300000
    )

    click_all_in_new_tabs(context, page)

    input("Press Enter to close...")
    browser.close()