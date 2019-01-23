# -*- coding: utf-8 -*-

"""UI tests for the queries page."""

import typing

import pytest

from models.user import User
from pages.home import HomePage
from pages.login import LoginPage


@pytest.mark.parametrize(
    "search_term, description",
    [
        ("Default Query", "Test default query for redash UI tests."),
        ("Ashleys Query", "Query created by Ashley."),
    ],
)
def test_query_by_username(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    search_term: str,
    description: str,
    user: User,
) -> None:
    """Search for query by username."""
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(search_term)
    query = search.queries[0].click()
    assert query.description == description


@pytest.mark.parametrize(
    "search_term, description",
    [
        ("Default Query", "Test default query for redash UI tests."),
        ("Ashleys Query", "Query created by Ashley."),
    ],
)
def test_query_by_description(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    search_term: str,
    description: str,
    user: User,
) -> None:
    """Search for query using description."""
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(description)
    query = search.queries[0].click()
    assert query.description == description


def test_query_by_weird_capitalization(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    org: str,
    user: User,
    variables: typing.Dict,
) -> None:
    """Search for query with weird capitalization."""
    term = variables[org]["queries"]["capitalization"]
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(term["name"])
    query = search.queries[0].click()
    assert query.description == term["description"]


def test_query_by_number(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    org: str,
    user: User,
    variables: typing.Dict,
) -> None:
    """Search for query with numbers in the name."""
    term = variables[org]["queries"]["numbers"]
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(term["name"])
    query = search.queries[0].click()
    assert query.description == term["description"]


def test_query_by_special_char(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    org: str,
    user: User,
    variables: typing.Dict,
) -> None:
    """Search for query wioth special characters in name."""
    term = variables[org]["queries"]["special-char"]
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(term["name"])
    query = search.queries[0].click()
    assert query.description == term["description"]


def test_search_for_unpublished_query(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    root_user: User,
) -> None:
    """Publish a query and then search for the unpublished one."""
    page = login_page.login(email=root_user.email, password=root_user.password)
    search = page.search("Publish Query")
    query = search.queries[0].click()
    query.publish()
    page = HomePage(selenium, server_url).open()
    search = page.search("Ashleys Query")
    query = search.queries[0].click()
    assert query.description == "Query created by Ashley."


def test_search_for_query_by_id(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    user: User,
) -> None:
    """Search for a query by its id."""
    page = login_page.login(email=user.email, password=user.password)
    search = page.search("2")
    query = search.queries[0].click()
    assert query.description == "Query created by Ashley."


def test_search_for_query_only_includes_search_result(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    user: User,
) -> None:
    page = login_page.login(email=user.email, password=user.password)
    search = page.search("Default Query")
    assert len(search.queries) == 2
    assert search.queries[0].link.text == "Default Query"


def test_change_query_title(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    root_user: User,
    variables: typing.Dict,
) -> None:
    page = login_page.login(email=root_user.email, password=root_user.password)
    query_specs = variables["default"]["queries"]["edit-query"]
    query_name = query_specs["name"]
    search = page.search(query_name)
    query = search.queries[0].click()
    assert query.title == query_name
    query.edit_title("NEW")
    assert query.title == f"{query_name} NEW"


def test_change_query_description(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    root_user: User,
) -> None:
    page = login_page.login(email=root_user.email, password=root_user.password)
    search = page.search("Blank Query")
    query = search.queries[0].click()
    query.edit_description("This is a description")
    assert query.description == "This is a description"


def test_edit_query_description(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    root_user: User,
    variables: typing.Dict,
) -> None:
    default_description = variables["default"]["queries"]["default"]["description"]
    page = login_page.login(email=root_user.email, password=root_user.password)
    search = page.search("Default Query")
    query = search.queries[0].click()
    assert query.description == default_description
    query.edit_description(" NEW NEW")
    assert query.description == f"{default_description} NEW NEW"


def test_edit_query_source(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    root_user: User,
    variables: typing.Dict,
) -> None:
    page = login_page.login(email=root_user.email, password=root_user.password)
    search = page.search("Default Query")
    query = search.queries[0].click()
    query.edit_source_button.click()
    assert "/source" in selenium.current_url


def test_query_fork(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    root_user: User,
    variables: typing.Dict,
) -> None:
    page = login_page.login(email=root_user.email, password=root_user.password)
    search = page.search("Default Query")
    query = search.queries[0].click()
    fork_query = query.click_dropdown_menu(text="Fork")
    selenium.switch_to.window(selenium.window_handles[-1])
    assert "Copy of (#4)" in fork_query.title


def test_query_archive(
    create_queries: typing.Callable[..., None],
    login_page: LoginPage,
    server_url: str,
    selenium,
    root_user: User,
    variables: typing.Dict,
) -> None:
    page = login_page.login(email=root_user.email, password=root_user.password)
    search = page.search("Archive Query")
    query = search.queries[0].click()
    query.click_dropdown_menu(text="Archive")
    assert query.query_tag == "Archived"
