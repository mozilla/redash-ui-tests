# -*- coding: utf-8 -*-

"""Plugin for running UI tests."""

import os

import attr
import pytest

from pages.login import LoginPage


@attr.s
class User:
    """User represents a Redash user."""
    name = attr.ib(type=str)
    password = attr.ib(type=str)
    email = attr.ib(type=str)


@pytest.fixture(name='org')
def fixture_org():
    """Return the slug of an org."""
    return 'default'


@pytest.fixture(name='unknown_user')
def fixture_unknown_user(variables, org):
    """Return a user that is not registered."""
    return User(**variables[org]['users']['unknown'])


@pytest.fixture(name='user')
def fixture_user(variables, org):
    """Return a registered user."""
    return User(**variables[org]['users']['ashley'])


@pytest.fixture(name='server_url')
def fixture_server_url(request):
    """Return the URL to the Redash server."""
    return request.config.option.server_url


@pytest.fixture(name='login_page')
def fixture_login_page(selenium, server_url, org):
    """Return a page object model for the login page."""
    login_page = LoginPage(selenium, server_url, org=org)
    return login_page.open()


def pytest_addoption(parser):
    """Add custom options to pytest."""
    group = parser.getgroup('redash')

    group.addoption(
        '--server-url',
        action='store',
        dest='server_url',
        type=str,
        default=os.getenv('REDASH_SERVER_URL', 'http://localhost:5000'),
        help="URL to the Redash Server",
    )
