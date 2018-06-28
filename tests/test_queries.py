# -*- coding: utf-8 -*-

"""UI tests for the queries page."""

import pytest

from models.user import User
from pages.login import LoginPage


@pytest.mark.parametrize(
    "search_term, description",
    [
        ("Default Query", "Test query for redash UI tests."),
        ("Ashleys Query", "Query created by Ashley."),
    ],
)
def test_query(
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
