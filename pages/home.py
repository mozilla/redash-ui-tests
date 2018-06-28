# -*- coding: utf-8 -*-

"""Page model for home page."""

import typing

from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from pages.queries import QueryPage

Selector = typing.Tuple[typing.Any, str]


class HomePage(Page):
    """Page object model for home page."""

    _profile_username_dropdown_locator: Selector = (
        By.CSS_SELECTOR,
        ".dropdown--profile__username",
    )
    _navbar_search_input_locator: Selector = (
        By.CLASS_NAME,
        "navbar__search__input",
    )
    _search_input_btn_locator: Selector = (
        By.CLASS_NAME,
        "input-group-btn .btn",
    )

    @property
    def loaded(self) -> HomePage:
        self.wait.until(
            lambda _: self.is_element_displayed(
                *self._profile_username_dropdown_locator
            )
        )
        return self

    @property
    def title(self) -> typing.Any:
        """Return the page title."""
        return self.wait.until(lambda s: self.selenium.title)

    @property
    def profile_dropdown(self) -> typing.Any:
        """Return the profile dropdown element."""
        element = self.wait.until(
            expected.visibility_of_element_located(
                self._profile_username_dropdown_locator
            )
        )
        return element.text

    def log_out(self) -> None:
        element = self.selenium.find_element(
            *self._profile_username_dropdown_locator
        )
        element.click()
        logout = element.find_elements_by_tag_name("li")
        logout[-1].click()

    def search(self, term: str) -> typing.Any:
        element = self.selenium.find_element(
            *self._navbar_search_input_locator
        )
        element.click()
        element.send_keys(term)
        button = self.selenium.find_element(*self._search_input_btn_locator)
        button.click()

        return QueryPage(self.selenium).wait_for_page_to_load()
