# -*- coding: utf-8 -*-

"""Page model for the queries page."""

from pypom import Page, Region

from selenium.webdriver.common.by import By


class QueryPage(Page):

    _query_table_locator = (By.TAG_NAME, "table")
    _table_row_locator = (By.TAG_NAME, "tr")

    @property
    def queries(self):
        table = self.selenium.find_element(*self._query_table_locator)
        items = table.find_elements(*self._table_row_locator)
        return [self.QueryRow(self, item) for item in items]

    class QueryRow(Region):

        _query_link_locator = (By.CSS_SELECTOR, "td a")

        @property
        def link(self):
            return self.selenium.find_element(*self._query_link_locator)

        def click(self):
            self.link.click()
            return QueryDetailPage(self.selenium)


class QueryDetailPage(Page):

    _query_description_locator = (By.CSS_SELECTOR, ".edit-in-place p")

    @property
    def description(self):
        return self.find_element(*self._query_description_locator).text
