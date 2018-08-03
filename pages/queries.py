# -*- coding: utf-8 -*-

"""Page model for the queries page."""

import typing

from pypom import Page, Region
from selenium.webdriver.common.by import By

Locator = typing.Tuple[typing.Any, str]


class QueryDetailPage(Page):

    _query_description_locator: Locator = (By.CSS_SELECTOR, ".edit-in-place p")
    _query_publish_button_locator: Locator = (By.CSS_SELECTOR, ".btn-publish")

    @property
    def description(self) -> typing.Any:
        return self.find_element(*self._query_description_locator).text

    def publish(self):
        self.find_element(*self._query_publish_button_locator).click()


class QueryRow(Region):

    _query_link_locator: Locator = (By.CSS_SELECTOR, "td a")

    @property
    def link(self) -> typing.Any:
        return self.selenium.find_element(*self._query_link_locator)

    def click(self) -> QueryDetailPage:
        self.link.click()
        return QueryDetailPage(self.selenium)


class QueryPage(Page):

    URL_TEMPLATE = '{server_url}/{queries}'

    _query_table_locator: Locator = (By.TAG_NAME, "table")
    _table_row_locator: Locator = (By.TAG_NAME, "tr")

    @property
    def queries(self) -> typing.List[QueryRow]:
        table = self.selenium.find_element(*self._query_table_locator)
        items = table.find_elements(*self._table_row_locator)
        return [QueryRow(self, item) for item in items]
