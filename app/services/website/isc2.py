import logging

from playwright.sync_api import Page, expect


class Isc2Page:
    def __init__(self, page: Page):
        self.page = page

    def close(self):
        self.page.close()

    def login(self, id, pw):
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

    def visit_watching_page(self, url, elapsed_time):
        self.page.goto(url)

        self.page.wait_for_selector("#onetrust-accept-btn-handler")
        self.page.click("#onetrust-accept-btn-handler")

        self.page.wait_for_timeout(10000)

        self.page.mouse.wheel(0, 500)
        self.page.mouse.wheel(0, 500)
        self.page.wait_for_timeout(1000)

        # scroll bottom
        # sitemap = self.page.get_by_role("link", name="Sitemap")
        # expect(sitemap).to_be_visible()
        # sitemap.scroll_into_view_if_needed()

        watch = self.page.frame_locator("#bt-player-wrapper-iframe").get_by_role(
            "button",
            name="Enter",
            # name="Register",
        )
        expect(watch).to_be_visible()
        watch.scroll_into_view_if_needed()
        watch.click()

        logging.info(f"Watching...")

        self.page.wait_for_timeout(int(elapsed_time) * 1000)

        logging.info(f"Done watching...")

        # 디버깅
        # self.page.pause()
