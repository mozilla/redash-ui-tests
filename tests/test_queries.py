# -*- coding: utf-8 -*-

"""UI tests for the queries page."""

import pytest

from models.user import User
from pages.home import HomePage
from pages.login import LoginPage


@pytest.mark.parametrize(
    "search_term, description",
    [
        ("Default Query", "Test query for redash UI tests."),
        ("Ashleys Query", "Query created by Ashley."),
    ],
)
def test_query_by_username(
    create_queries,
    login_page: LoginPage,
    search_term: str,
    description: str,
    user: User,
) -> None:
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(search_term)
    query = search.queries[0].click()
    assert query.description == description


@pytest.mark.parametrize(
    "search_term, description",
    [
        ("Default Query", "Test query for redash UI tests."),
        ("Ashleys Query", "Query created by Ashley."),
    ],
)
def test_query_by_description(
    create_queries,
    login_page: LoginPage,
    search_term: str,
    description: str,
    user: User,
) -> None:
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(description)
    query = search.queries[0].click()
    assert query.description == description


def test_query_by_weird_capitalization(
    create_queries,
    login_page: LoginPage,
    org,
    user: User,
    variables,
) -> None:
    term = variables[org]["queries"]["capitalization"]
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(term["name"])
    query = search.queries[0].click()
    assert query.description == term["description"]


def test_query_by_number(
    create_queries,
    login_page: LoginPage,
    org,
    user: User,
    variables,
) -> None:
    term = variables[org]["queries"]["numbers"]
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(term['name'])
    query = search.queries[0].click()
    assert query.description == term["description"]


def test_query_by_special_char(
    create_queries,
    login_page: LoginPage,
    org,
    user: User,
    variables,
) -> None:
    term = variables[org]["queries"]["special-char"]
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(term['name'])
    query = search.queries[0].click()
    assert query.description == term["description"]



def test_search_for_unpublished_query(
    create_queries,
    login_page: LoginPage,
    server_url,
    selenium,
    user: User,
) -> None:
    """Publish a query and then search for the unpublished one."""
    page = login_page.login(email=user.email, password=user.password)
    search = page.search("Publish Query")
    query = search.queries[0].click()
    query.publish()
    page = HomePage(selenium, server_url).open()
    search = page.search("Ashleys Query")
    query = search.queries[0].click()
    assert query.description == "Query created by Ashley."
