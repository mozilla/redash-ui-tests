# -*- coding: utf-8 -*-

"""Page object models for Redash."""


@attr.s(auto_attribs=True)
class User:
    """User represents a Redash user."""

    name: str
    password: str
    email: str
    _id: int


@attr.s(auto_attribs=True)
class UserFactory:
    """UserFactory provides an interface to create Redash users."""

    users: typing.List[User] = attr.Factory(list)

    def __iter__(self) -> typing.Generator[User, None, None]:
        for user in self.users:
            yield user

    def __contains__(self, user: User) -> bool:
        return user in self.users

    def create_user(self, **kwargs: typing.Any) -> User:
        user = User(**kwargs)
        self.users.append(user)
        return user
