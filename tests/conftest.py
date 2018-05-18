# -*- coding: utf-8 -*-

"""Plugin for running UI tests."""

import os

import attr
import pytest
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from pages.login import LoginPage


@attr.s
class User:
    """User represents a Redash user."""
    name = attr.ib(type=str)
    password = attr.ib(type=str)
    email = attr.ib(type=str)


@pytest.fixture(scope='session', autouse=True)
def _verify_url(request, base_url, user, org):
    """Verifies the base URL.
    
    This will ping the base url until it returns a 200.
    """
    verify = request.config.option.verify_base_url
    if base_url and verify:
        session = requests.Session()
        retries = Retry(backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        session.mount(base_url, HTTPAdapter(max_retries=retries))
        session.get(base_url, verify=False)


@pytest.fixture(name='org', scope='session')
def fixture_org():
    """Return the slug of an org."""
    return 'default'


@pytest.fixture(name='unknown_user')
def fixture_unknown_user(variables, org):
    """Return a user that is not registered."""
    return User(**variables[org]['users']['unknown'])


@pytest.fixture(name='user', scope='session')
def fixture_user(variables, org):
    """Return a registered user."""
    return User(**variables[org]['users']['ashley'])


@pytest.fixture(name='login_page')
def fixture_login_page(selenium, base_url, org):
    """Return a page object model for the login page."""
    login_page = LoginPage(selenium, base_url, org=org)
    return login_page.open()
