# -*- coding: utf-8 -*-

"""Plugin for running UI tests."""

import os
import typing

import pytest
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from pages.login import LoginPage
from models.user import UserFactory, User


@pytest.fixture(name="user_factory", scope="session")
def fixture_user_factory() -> UserFactory:
    return UserFactory()


@pytest.fixture(autouse=True)
def _verify_url(request, server_url: str, user: User, org: str) -> None:
    """Verifies the base URL.

    This will ping the base url until it returns a 200.
    """
    if server_url and request.config.option.verify_server_url:
        session = Session()
        retries = Retry(
            backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )
        session.mount(server_url, HTTPAdapter(max_retries=retries))
        session.get(server_url, verify=False)


@pytest.fixture(name="server_url", scope="session")
def fixture_server_url(request) -> typing.Any:
    """Return the URL to the Redash server."""
    return request.config.getoption("server_url")


@pytest.fixture(name="org", scope="session")
def fixture_org() -> str:
    """Return the slug of an org."""
    return "default"


@pytest.fixture(name="unknown_user")
def fixture_unknown_user(variables: typing.Dict, org: str) -> User:
    """Return a user that is not registered."""
    return User(**variables[org]["users"]["unknown"])


@pytest.fixture(name="user", scope="session")
def fixture_user(
    create_user: typing.Callable[..., User],
    variables: typing.Dict,
    org: str,
    user_factory: UserFactory,
) -> User:
    """Return a registered user."""

    user_info = variables[org]["users"]["ashley"]

    for user in user_factory:
        if user.email == user_info["email"]:
            return user

    return create_user(**user_info)


@pytest.fixture(name="users", scope="session")
def fixture_users(
    variables: typing.Dict,
    org: str,
    root_session,
    server_url: str,
    user_factory: UserFactory,
) -> typing.List[User]:
    # Check if there are any users in the db, if not, Redash needs to be set up
    response = root_session.get(f"{server_url}/api/users")
    if response.status_code == 404:
        raise RuntimeError(
            "Root user must be created. Please run 'make setup-redash'"
        )

    for existing_user in response.json():
        for user in variables[org]["users"].values():
            if user["email"] == existing_user["email"]:
                user_factory.create_user(
                    name=user["name"],
                    password=user["password"],
                    email=user["email"],
                    id=existing_user["id"],
                )

    return user_factory.users


@pytest.fixture(name="root_user", scope="session")
def fixture_root_user(variables: typing.Dict, org: str) -> User:
    """Return the root user used for setup."""
    return User(**variables[org]["users"]["rootuser"])


@pytest.fixture(name="login_page")
def fixture_login_page(selenium, server_url: str, org: str) -> typing.Any:
    """Return a page object model for the login page."""
    login_page = LoginPage(selenium, server_url, org=org)
    return login_page.open()


@pytest.fixture(name="create_user", scope="session")
def fixture_create_user(
    root_session: Session, server_url: str, user_factory: UserFactory
) -> typing.Callable:
    """Return a function to create a user."""

    def create_user(
        name: str = "", email: str = "", password: str = ""
    ) -> User:
        """Create a user via the Redash API.

        This will use the authenticated root user requests session to create
        a user, accept the invite, and add a password.

        Args:
            server_url:
                URL for redash instance
            session:
                Requests login session.
                This is needed to allow for user creation.
            user:
                User object that will be created.

        """
        # look up user by email and return if found. If not, create user.
        response = root_session.get(f"{server_url}/api/users")
        for user in response.json():
            if user["email"] == email:
                return user_factory.create_user(
                    name=name, password=password, email=email, id=user["id"]
                )

        response = root_session.post(
            f"{server_url}/api/users",
            json={"name": name, "email": email, "no_invite": True},
        )
        if response.status_code != 200:
            raise RuntimeError(f"unable to create user: {response.text}")

        # add passwod to user
        try:
            invite_link = response.json()["invite_link"]
            response = root_session.post(
                f"{server_url}{invite_link}", data={"password": password}
            )
        except KeyError:
            raise RuntimeError(f"no invite link found. {response.text}")
        except Exception:
            raise RuntimeError(f"error sending invite: {response.text}")

        return user_factory.create_user(
            name=name, email=email, password=password
        )

    return create_user


@pytest.fixture(name="root_session", scope="session")
def fixture_root_session(server_url: str, root_user: User) -> Session:
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
    session = Session()
    response = session.post(
        url, data={"email": root_user.email, "password": root_user.password}
    )
    if response.status_code != 200:
        raise RuntimeError(f"unable to log in as root user: {response.text}")
    return session


@pytest.fixture(name="create_queries", scope="session")
def fixture_create_queries(
    root_session: Session, server_url: str, variables: typing.Dict
) -> None:
    """Create 2 queries using the data from variables.json."""

    # Check if query exists, if so, do not create it again
    response = root_session.get(f"{server_url}/api/queries")
    for item in response.json()["results"]:
        for values in variables["default"]["queries"].values():
            if item["name"] in values.values():
                return

    for query in variables["default"]["queries"].values():
        response = root_session.post(f"{server_url}/api/queries", json=query)
        if response.status_code != 200:
            raise RuntimeError(f"unable to log create query: {response.text}")


def pytest_addoption(parser) -> None:
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
