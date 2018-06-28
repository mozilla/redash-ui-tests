# -*- coding: utf-8 -*-

"""UI tests for the login page."""

import pytest
from selenium.common.exceptions import TimeoutException

from models.user import User
from pages.login import LoginPage


@pytest.mark.nondestructive
def test_login_wrong_user_credentials(
    login_page: LoginPage, unknown_user: User
) -> None:
    """Test for a failed login attempt."""
    assert login_page.title == "Login to Redash"

    with pytest.raises(TimeoutException):
        login_page.login(
            email=unknown_user.email, password=unknown_user.password
        )

    assert login_page.alert == "Wrong email or password."
    assert login_page.title == "Login to Redash"


@pytest.mark.nondestructive
def test_login(login_page: LoginPage, user: User) -> None:
    """Test for a successful login attempt."""
    assert login_page.title == "Login to Redash"

    home_page = login_page.login(email=user.email, password=user.password)

    assert home_page.profile_dropdown == user.name
    assert home_page.title == "Redash"
