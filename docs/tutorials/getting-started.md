# Getting started

The goal of this tutorial is to set up **redash-ui-tests** on your local
machine, learn how to run the tests and see what happens if a test is broken.

## Set up environment

### Install software

We use [Docker][docker] and [docker-compose][docker-compose] for running the
UI tests in an isolated and reproducable environment. This means that our
[continuous integration][ci] server runs the tests in the same way that we do
locally, which makes it easier to investigate issues.

Please check out the installation instructions for your platform for
[Docker][docker-install] and [docker-compose][docker-compose-install].

We manage the source code for **redash-ui-tests** with the [git][git] version
control system and host it on [GitHub][github]. You might have git already
installed on your system, but if you don't see the [downloads
page][git-downloads].

### Clone project

Open a terminal and type ``git clone`` and the URL to **redash-ui-tests**:

```text
$ git clone https://github.com/mozilla/redash-ui-tests
```

This will download the latest version of the source code to your local
machine to a new directory named ``redash-ui-tests``.

Navigate to the project:

```text
$ cd redash-ui-tests
```

When you're ready dive right into the next steps to learn about how to work
with the tests.

## Run the test suite

🚧 **TODO**

## Break a test

🚧 **TODO**

[ci]: https://circleci.com/gh/mozilla/redash-ui-tests/
[docker-compose-install]: https://docs.docker.com/compose/install/
[docker-compose]: https://docs.docker.com/compose/
[docker-install]: https://docs.docker.com/install/
[docker]: https://docs.docker.com/
[git-downloads]: https://git-scm.com/downloads
[git]: https://git-scm.com/
[github]: https://github.com/
