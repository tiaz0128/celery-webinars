import logging
from typing import Literal

import os
from dotenv import load_dotenv


from app.services.website.bright_talk import BrightTalkPage
from app.services.website.isc2 import Isc2Page
from run import app

from playwright.sync_api import Browser, sync_playwright, Page

load_dotenv()


@app.task(queue="webinars")
def run_web_page_task(url: str, elapsed_time: str) -> Literal["Success", "Fail"]:
    logging.info(f"{url=}, {elapsed_time=}")

    brighttalk_id = os.getenv("BRIGHTTALK_USERNAME")
    brighttalk_pw = os.getenv("BRIGHTTALK_PASSWORD")

    isc2_id = os.getenv("ISC2_USERNAME")
    isc2_pw = os.getenv("ISC2_PASSWORD")

    with sync_playwright() as p:
        try:
            browser: Browser = p.chromium.launch(headless=False)

            page: Page = browser.new_page()

            bright_talk_page = BrightTalkPage(page)
            isc2 = Isc2Page(page)

            bright_talk_page.login(brighttalk_id, brighttalk_pw)

            isc2.login(isc2_id, isc2_pw)
            isc2.visit_watching_page(url, elapsed_time)

            return "Watching Webinar Success"

        except Exception as e:
            logging.info(f"Fail: {e}")
            return "Watching Webinar Fail"

        finally:
            isc2.close()
            browser.close()
