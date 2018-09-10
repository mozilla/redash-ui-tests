# -*- coding: utf-8 -*-

"""Page model for the queries page."""

import typing

from pypom import Page, Region
from selenium.webdriver.common.by import By

Locator = typing.Tuple[typing.Any, str]


class QueryDetailPage(Page):

    _query_description_locator: Locator = (
        By.CSS_SELECTOR,
        "edit-in-place:nth-child(1) > span:nth-child(1) > p:nth-child(1)",
    )
    _query_publish_button_locator: Locator = (By.CSS_SELECTOR, ".btn-publish")

    @property
    def description(self) -> typing.Any:
        return self.find_element(*self._query_description_locator).text

    def publish(self):
        self.find_element(*self._query_publish_button_locator).click()


class QueryRow(Region):

    _query_link_locator: Locator = (By.CSS_SELECTOR, ".table-main-title a")

    @property
    def link(self) -> typing.Any:
        return self.selenium.find_element(*self._query_link_locator)

    def click(self) -> QueryDetailPage:
        self.link.click()
        return QueryDetailPage(self.selenium)


class QueryPage(Page):

    URL_TEMPLATE = "{server_url}/{queries}"

    _query_table_locator: Locator = (By.CSS_SELECTOR, ".table")
    _table_row_locator: Locator = (By.TAG_NAME, "tr")

    def wait_for_page_to_load(self) -> QueryPage:
        self.wait.until(lambda _: self.is_element_displayed(*self._query_table_locator))
        return self

    @property
    def queries(self) -> typing.List[QueryRow]:
        table = self.selenium.find_element(*self._query_table_locator)
        items = table.find_elements(*self._table_row_locator)
        return [QueryRow(self, item) for item in items]
