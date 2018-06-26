# -*- coding: utf-8 -*-

"""Page model for home page."""

from pypom import Page

from selenium.webdriver.common.by import By


class HomePage(Page):
    """Page object model for home page."""

    def wait_for_page_to_load(self):
        self.wait.until(
            lambda _: self.is_element_displayed(
                By.CSS_SELECTOR, ".dropdown--profile__username"
            )
        )
        return self

    def log_out(self):
        element = self.selenium.find_element_by_css_selector(
            ".dropdown .dropdown--profile__username"
        )
        element.click()
        logout = element.find_elements_by_tag_name("li")
        logout[-1].click()

    def search(self, term):
        element = self.selenium.find_element_by_css_selector(".navbar__search__input")
        element.click()
        element.send_keys(term)
        button = self.selenium.find_element_by_css_selector(".input-group-btn .btn")
        button.click()
        from pages.queries import QueryPage

        return QueryPage(self.selenium).wait_for_page_to_load()
