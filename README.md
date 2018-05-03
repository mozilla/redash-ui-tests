# redash-ui-tests

 :bar_chart: UI tests for Redash

## Description

The goal of this project is to add UI test coverage for the [Redash
project][redash], so that we automatically detect regressions in UI
functionality and reduce the time we spend in manual testing. This will
ultimately help us develop more quickly, reduce time between releases and
free up our QA Engineers to focus on specific test cases and complex issues.

## Requirements

We use [Selenium][selenium] for interacting with [Firefox][firefox] and the
Redash web UI. Tests are developed in [Python 3.6][python] using the
[pytest][pytest] testing framework.

We run the UI tests inside a [Docker][docker] container with
[Ubuntu][ubuntu]. Please install Docker to run the UI tests on your local
machine.

## Running the tests

Clone the [git][git] repository:

```text
git clone git@github.com:hackebrot/redash-ui-tests.git
```

Navigate to the project:

```text
cd redash-ui-tests
```

Build the Docker image:

```bash
docker build -t "redash-ui-tests" .
```

Next you want to run the tests in a new container. You need a URL pointing to
a running [Redash][redash] server instance, which could either be a hosted
version or a local development instance.

Replace ``<REDASH_SERVER_URL>`` in the following command with the URL to
Redash, for example: ``http://localhost:5000``.

```bash
docker run \
    --net="host" \
    --env REDASH_SERVER_URL="<REDASH_SERVER_URL>" \
    --mount type=bind,source="$(pwd)",target=/home/user/src \
    "redash-ui-tests"
```

We also maintain a [Makefile][makefile] for these commands:

```text
bash       Run bash in container as user
build      Build Docker image
clean      Delete pyc files
tests      Run tests in container
```

## Contributing

Every contribution helps to make redash-ui-tests better. Any help is greatly
appreciated and credit will always be given!

Please check out the [good first issue][first] label for tasks, that are good
candidates for your first contribution to redash-ui-tests!

[docker]: https://docs.docker.com/install/
[firefox]: https://www.mozilla.org/en-US/firefox/new/
[first]: https://github.com/hackebrot/redash-ui-tests/labels/good%20first%20issue
[git]: https://git-scm.com/
[makefile]: /Makefile
[pytest]: https://docs.pytest.org/en/latest/
[python]: https://www.python.org/
[redash]: https://github.com/getredash/redash
[selenium]: https://pypi.org/project/selenium/
[ubuntu]: https://www.ubuntu.com/
