# Developing tests

We use [Selenium][selenium] for interacting with [Firefox][firefox] and the
Redash web UI. Tests are developed in [Python 3.6][python] using the
[pytest][pytest] testing framework.

We run the UI tests inside a [Docker][docker] container with
[Ubuntu][ubuntu]. Please install Docker to run the UI tests on your local
machine.

🚧 **TODO**

[docker]: https://docs.docker.com/
[firefox]: https://www.mozilla.org/en-US/firefox/new/
[pytest]: https://docs.pytest.org/en/latest/
[python]: https://www.python.org/
[selenium]: https://pypi.org/project/selenium/
[ubuntu]: https://www.ubuntu.com/
