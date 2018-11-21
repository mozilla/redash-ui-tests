# -*- coding: utf-8 -*-

"""Page model for the queries page."""

import typing

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

Locator = typing.Tuple[typing.Any, str]


class QueryDetailPage(Page):

    _query_modal_archive_locator: Locator = (
        By.CSS_SELECTOR,
        ".modal-footer > button:nth-child(2)",
    )
    _query_description_locator: Locator = (
        By.CSS_SELECTOR,
        "div.query-metadata:nth-child(3) > edit-in-place:nth-child(1)",
    )
    _query_description_blank_locator: Locator = (
        By.CSS_SELECTOR,
        "div.query-metadata:nth-child(3) > "
        "edit-in-place:nth-child(1) > span:nth-child(2)",
    )
    _query_description_edit_locator: Locator = (
        By.CSS_SELECTOR,
        "edit-in-place:nth-child(1) > textarea.rd-form-control",
    )
    _query_edit_source_locator: Locator = (
        By.CSS_SELECTOR,
        ".source-control a.btn-default:nth-child(1)",
    )
    _query_dropdown_menu_locator: Locator = (
        By.CSS_SELECTOR,
        ".source-control .dropdown",
    )
    _query_dropdown_menu_item_locator: Locator = (By.CSS_SELECTOR, "ul > li > a")
    _query_name_locator: Locator = (
        By.CSS_SELECTOR,
        ".page-title > h3:nth-child(2) > "
        "edit-in-place:nth-child(1) > span:nth-child(1)",
    )
    _query_name_edit_locator: Locator = (
        By.CSS_SELECTOR,
        ".page-title > h3:nth-child(2) > "
        "edit-in-place:nth-child(1) > input.rd-form-control",
    )
    _query_publish_button_locator: Locator = (By.CSS_SELECTOR, ".btn-publish")
    _query_tag_locator: Locator = (
        By.CSS_SELECTOR,
        ".page-header--query .page-title span.label",
    )

    @property
    def description(self) -> typing.Any:
        return self.find_element(*self._query_description_locator).text

    def click_dropdown_menu(self, text=None) -> typing.Any:
        menu = self.find_element(*self._query_dropdown_menu_locator)
        items = menu.find_elements(*self._query_dropdown_menu_item_locator)
        menu.click()
        for item in (i for i in items if i.text in text):
            if text == "Fork":
                item.click()
                page = QueryDetailPage(self.selenium, self.base_url)
                return page.wait_for_page_to_load()
            if text == "Archive":
                item.click()
                self.find_element(*self._query_modal_archive_locator).click()
                return
        raise ValueError(f"{item} was not found within the dropdown menu.")

    def edit_description(self, description: str) -> None:
        try:
            self.find_element(*self._query_description_blank_locator).click()
        except Exception:
            self.find_element(*self._query_description_locator).click()
        element = self.find_element(*self._query_description_edit_locator)
        element.send_keys(f" {description}")
        element.send_keys(Keys.ENTER)

    @property
    def edit_source_button(self) -> typing.Any:
        return self.find_element(*self._query_edit_source_locator)

    def edit_title(self, title: str) -> None:
        element = self.find_element(*self._query_name_locator)
        element.click()
        element = self.find_element(*self._query_name_edit_locator)
        element.send_keys(f" {title}")
        element.send_keys(Keys.ENTER)

    def publish(self):
        self.find_element(*self._query_publish_button_locator).click()

    @property
    def query_tag(self) -> typing.Any:
        return self.find_element(*self._query_tag_locator).text

    @property
    def title(self) -> typing.Any:
        self.wait.until(
            lambda _: self.find_element(*self._query_name_locator).is_displayed()
        )
        return self.find_element(*self._query_name_locator).text


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

    def wait_for_page_to_load(self) -> typing.Any:
        self.wait.until(lambda _: self.is_element_displayed(*self._query_table_locator))
        return self

    @property
    def queries(self) -> typing.List[QueryRow]:
        table = self.selenium.find_element(*self._query_table_locator)
        items = table.find_elements(*self._table_row_locator)
        return [QueryRow(self, item) for item in items]
