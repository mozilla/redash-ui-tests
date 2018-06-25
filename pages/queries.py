# -*- coding: utf-8 -*-

"""Page model for home page."""

from pypom import Page, Region

from selenium.webdriver.common.by import By


class QueryPage(Page):
    @property
    def queries(self):
        table = self.selenium.find_element(By.TAG_NAME, "table")
        items = table.find_elements(By.TAG_NAME, "tr")
        return [self.QueryRow(self, item) for item in items]

    class QueryRow(Region):
        @property
        def link(self):
            return self.selenium.find_element(By.CSS_SELECTOR, "td a")

        def click(self):
            self.link.click()
            return QueryDetailPage(self.selenium)


class QueryDetailPage(Page):
    @property
    def description(self):
        return self.find_element(By.CSS_SELECTOR, ".edit-in-place p").text
