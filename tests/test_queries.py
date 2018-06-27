import pytest


@pytest.mark.parametrize(
    "search_term, description",
    [
        ("Default Query", "Test query for redash UI tests."),
        ("Ashleys Query", "Query created by Ashley."),
    ],
)
def test_query(create_queries, description, login_page, search_term, user):
    page = login_page.login(email=user.email, password=user.password)
    search = page.search(search_term)
    query = search.queries[0].click()
    assert query.description == description
