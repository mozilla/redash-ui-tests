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
    _id = attr.ib(type=int, default=None)


@pytest.fixture(autouse=True)
def _verify_url(request, server_url, user, org):
    """Verifies the base URL.
    
    This will ping the base url until it returns a 200.
    """
    verify = request.config.option.verify_server_url
    if server_url and verify:
        session = requests.Session()
        retries = Retry(backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount(server_url, HTTPAdapter(max_retries=retries))
        session.get(server_url, verify=False)


@pytest.fixture(name="server_url", scope="session")
def fixture_server_url(request):
    """Return the URL to the Redash server."""
    return request.config.option.server_url


@pytest.fixture(name="org", scope="session")
def fixture_org():
    """Return the slug of an org."""
    return "default"


@pytest.fixture(name="unknown_user")
def fixture_unknown_user(variables, org):
    """Return a user that is not registered."""
    return User(**variables[org]["users"]["unknown"])


@pytest.fixture(name="user", scope="session")
def fixture_user(create_user, variables, org, users):
    """Return a registered user."""
    user_info = variables[org]["users"]["ashley"]
    for user in users:
        if user.email in user_info["email"]:
            return user
    return create_user(**user_info)


@pytest.fixture(name="users", scope="session")
def fixture_users(variables, org, root_session, server_url):
    response = root_session.get(f"{server_url}/api/users")
    # check if user has any users within db, if not, they must run setup
    if response.status_code == 404:
        raise RuntimeError("Root user must be created. Please run 'make setup-redash'")
    users = []
    for existing_user in response.json():
        for user in variables[org]["users"].values():
            if user["email"] == existing_user["email"]:
                users.append(
                    User(
                        user["name"],
                        user["password"],
                        user["email"],
                        existing_user["id"],
                    )
                )
    return users


@pytest.fixture(name="root_user", scope="session")
def fixture_root_user(variables, org):
    """Return the root user used for setup."""
    return User(**variables[org]["users"]["rootuser"])


@pytest.fixture(name="login_page")
def fixture_login_page(selenium, server_url, org):
    """Return a page object model for the login page."""
    login_page = LoginPage(selenium, server_url, org=org)
    return login_page.open()


@pytest.fixture(name="create_user", scope="session")
def fixture_create_user(root_session, server_url, users):
    """Return a function to create a user."""

    def create_user(name=None, email=None, password=None):
        """Create a user via api.

        This will use the authenticated root user requests session to create a
        user, accept the invite, and add a password.
    
        Args:
            server_url: 
                URL for redash instance
            session: 
                Requests login session. 
                This is needed to allow for user creation.
            user:
                User object that will be created.

        """
        data = {"name": name, "email": email, "no_invite": True}
        # look up user by email and return if found. If not, create user.
        reponse = root_session.get(f"{server_url}/api/users")
        for user in reponse.json():
            if user["email"] is email:
                return users[user["id"]]
        response = root_session.post(f"{server_url}/api/users", json=data)
        if response.status_code != 200:
            raise RuntimeError(f"unable to create user: {response.text}")
        # add passwod to user
        user_password = {"password": password}
        try:
            invite_link = f"{response.json()['invite_link']}"
            response = root_session.post(
                f"{server_url}{invite_link}", data=user_password
            )
        except KeyError:
            raise RuntimeError(f"no invite link found. {response.text}")
        except Exception:
            raise RuntimeError(f"error sending invite: {response.text}")
        return User(name=name, email=email, password=password)

    return create_user


@pytest.fixture(name="root_session", scope="session")
def fixture_root_session(server_url, root_user):
    """Root login.
    
    This is only used to authenticate api calls as admin. It will login as the
    root user and return a requests session that can be used to create/delete
    other users as well as other actions.

    Args:
        server_url:
            URL for redash instance.
        user:
            User object that will be created.

    Returns:
        session:
            Requests session used for api calls.

    """
    url = f"{server_url}/login"
    session = requests.Session()
    response = session.post(
        url, data={"email": root_user.email, "password": root_user.password}
    )
    if response.status_code != 200:
        raise RuntimeError(f"unable to log in as root user: {response.text}")
    return session


def pytest_addoption(parser):
    """Add custom options to pytest."""
    group = parser.getgroup("redash")

    group.addoption(
        "--server-url",
        action="store",
        dest="server_url",
        type=str,
        default=os.getenv("REDASH_SERVER_URL", "http://localhost:5000"),
        help="URL to the Redash Server",
    )
    group.addoption(
        "--verify-server-url",
        action="store_true",
        default=not os.getenv("VERIFY_SERVER_URL", "false").lower() == "false",
        help="verify the server url.",
    )
