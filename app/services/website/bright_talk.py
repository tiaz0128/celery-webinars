import logging

from playwright.sync_api import expect, Page


class BrightTalkPage:
    def __init__(self, page: Page):
        self.page = page

    def close(self):
        self.page.close()

    def login(self, id, pw):
        self.page.goto("https://www.brighttalk.com/login")
        self.page.wait_for_load_state("domcontentloaded")

        email = self.page.get_by_placeholder("Email")
        expect(email).to_have_attribute("id", "email")
        email.fill(id)

        self.page.get_by_role("button", name="Proceed").click()
        self.page.wait_for_timeout(3000)

        password = self.page.get_by_placeholder("Password")
        expect(password).to_have_attribute("id", "password")
        password.fill(pw)

        self.page.get_by_role("button", name="Log in").click()
        self.page.wait_for_timeout(10000)

        logging.info(f"Login Success : brighttalk.com")
