import logging
from typing import Literal

from run import app

from playwright.sync_api import Browser, sync_playwright, expect


@app.task(queue="work-page")
def work_page(url: str, id: str, pw: str) -> Literal["Success", "Fail"]:
    logging.info(f"{url=}, {id=}, {pw=}")

    with sync_playwright() as p:
        try:
            browser: Browser = p.chromium.launch(headless=False)

            isc2 = Isc2Page(browser)

            isc2.login_page(id, pw)
            isc2.visit_watching_page(url)

            return "Success"
        except Exception as e:
            return "Fail"
        finally:
            isc2.close()
            browser.close()


class Isc2Page:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.page = self.browser.new_page()

    def close(self):
        self.page.close()

    def login_page(self, id, pw):
        self.page.goto("https://my.isc2.org/s/login/")
        self.page.wait_for_load_state("domcontentloaded")

        username = self.page.locator('input[name="username"]')
        expect(username).to_have_attribute("name", "username")

        password = self.page.locator('input[name="password"]')
        expect(password).to_have_attribute("name", "password")

        username.fill(id)
        password.fill(pw)

        self.page.get_by_role("button", name="Sign In").click()

        self.page.wait_for_timeout(10000)

        logging.info(f"Login Success")
        # context = browser.new_context()
        # context.storage_state(path=".temp/isc2-session.json")

    def visit_watching_page(self, url):
        self.page.goto(url)

        self.page.wait_for_selector("#onetrust-accept-btn-handler")
        self.page.click("#onetrust-accept-btn-handler")

        self.page.wait_for_timeout(10000)

        # scroll bottom
        sitemap = self.page.get_by_role("link", name="Sitemap")
        expect(sitemap).to_be_visible()
        sitemap.scroll_into_view_if_needed()

        self.page.pause()
        watch = self.page.frame_locator("#bt-player-wrapper-iframe").get_by_role(
            "button",
            name="Register",
            # name="Watch",
        )
        expect(watch).to_be_visible()
        watch.scroll_into_view_if_needed()
        watch.click()

        logging.info(f"Watching...")

        self.page.wait_for_timeout(5000)

        logging.info(f"Done watching...")
