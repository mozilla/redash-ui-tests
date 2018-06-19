# redash-ui-tests

:bar_chart: UI tests for [Redash][redash]

## Description

[Redash][redash] is a open source web-application for working with data.
Users can query data from different sources, create visualizations and
dashboards, and share them in their organization. Please check out the
[knowledge base][redash help] for more info about the Redash project.

The **redash-ui-tests** project is a community effort to develop automated UI
tests for Redash. We want to be able to automatically detect UI regressions
in release candidates and reduce the time spent on manual testing. We will
gradually add more UI tests for functionality, that is important to our
users. Check out the [tests issue label][tests] to get an idea about test cases
that we are planning to automate.

## Project organization

We use GitHub features to organize our work on **redash-ui-tests**:

- [issues][issues] for keeping track of tasks, enhancements, and bugs
- [labels][labels] for categorizing issues and pull requests
- [milestones][milestones] for associating issues with project phases
- [project boards][projects] for tracking the progress of our work

## Contributing

Are you interested in developing UI tests in [Python][python], or helping us
improve our documentation, or have ideas for how to improve
**redash-ui-tests**?

Read our [contributing guide][contributing] and check out the [good first
issue][first] label for tasks, that are good candidates for your first
contribution to **redash-ui-tests**. Your contributions are greatly
appreciated! Every little bit helps, and credit will always be given!

Please note that **redash-ui-tests** is released with a [Contributor Code of
Conduct][code of conduct]. By participating in this project you agree to abide
by its terms.

## Development

We use [Selenium][selenium] for interacting with [Firefox][firefox] and the
Redash web UI. Tests are developed in [Python 3.6][python] using the
[pytest][pytest] testing framework.

We run the UI tests inside a [Docker][docker] container with
[Ubuntu][ubuntu]. Please install Docker to run the UI tests on your local
machine.

## Running the tests

Clone the [git][git] repository:

```text
git clone git@github.com:mozilla/redash-ui-tests.git
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

[code of conduct]: /.github/CODE_OF_CONDUCT.md
[contributing]: /.github/CONTRIBUTING.md
[docker]: https://docs.docker.com/install/
[firefox]: https://www.mozilla.org/en-US/firefox/new/
[first]: https://github.com/mozilla/redash-ui-tests/labels/good%20first%20issue
[git]: https://git-scm.com/
[issues]: https://github.com/mozilla/redash-ui-tests/issues
[labels]: https://github.com/mozilla/redash-ui-tests/labels
[makefile]: /Makefile
[milestones]: https://github.com/mozilla/redash-ui-tests/milestones
[projects]: https://github.com/mozilla/redash-ui-tests/projects
[pytest]: https://docs.pytest.org/en/latest/
[python]: https://www.python.org/
[redash help]: https://redash.io/help/
[redash]: https://github.com/getredash/redash
[selenium]: https://pypi.org/project/selenium/
[tests]: https://github.com/mozilla/redash-ui-tests/issues?q=is%3Aissue+is%3Aopen+label%3Atests
[ubuntu]: https://www.ubuntu.com/
