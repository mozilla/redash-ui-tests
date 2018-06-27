# -*- coding: utf-8 -*-

"""Page model for home page."""

from pypom import Page

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected


class HomePage(Page):
    """Page object model for home page."""

    _profile_username_dropdown_locator = (
        By.CSS_SELECTOR,
        ".dropdown--profile__username",
    )
    _navbar_search_input_locator = (By.CLASS_NAME, "navbar__search__input")
    _search_input_btn_locator = (By.CLASS_NAME, "input-group-btn .btn")

    @property
    def loaded(self):
        self.wait.until(
            lambda _: self.is_element_displayed(
                *self._profile_username_dropdown_locator
            )
        )
        return self

    @property
    def title(self):
        """Return the page title."""
        return self.wait.until(lambda s: self.selenium.title)

    @property
    def profile_dropdown(self):
        """Return the profile dropdown element."""
        element = self.wait.until(
            expected.visibility_of_element_located(
                self._profile_username_dropdown_locator
            )
        )
        return element.text

    def log_out(self):
        element = self.selenium.find_element(
            *self._profile_username_dropdown_locator
        )
        element.click()
        logout = element.find_elements_by_tag_name("li")
        logout[-1].click()

    def search(self, term):
        element = self.selenium.find_element(
            *self._navbar_search_input_locator
        )
        element.click()
        element.send_keys(term)
        button = self.selenium.find_element(*self._search_input_btn_locator)
        button.click()
        from pages.queries import QueryPage

        return QueryPage(self.selenium).wait_for_page_to_load()
