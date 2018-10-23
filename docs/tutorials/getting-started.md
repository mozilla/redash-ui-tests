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

#### Redash Setup

The redash instance must be setup before running the tests. Start the images
``docker-compose up -d`` in the root of the directory in which the project
was downloaded to. This will download the images if you don't have them. It
will also start the container in the background. You can view the status of
the containers via ``docker-compose ps``. You can also stop the docker
container by running ``docker-compose stop``.

All the following commands should also be run within the same directory that
you downloaded the project to.

Run these following commands to setup Redash:

1. Create database:

```text
docker-compose run --rm server create_db
```

2. Create test database:

```text
docker-compose run --rm postgres psql -h postgres -U postgres -c "create database tests"
```

3. Create a default user named ``rootuser`` with a password ``IAMROOT`` and
an organization ``default``:

```text
docker-compose run --rm server /app/manage.py users create_root root@example.com "rootuser" --password "IAMROOT" --org default
```

4. Create a new data source named ``ui-tests``.

```text
docker-compose run --rm server /app/manage.py ds new "ui-tests" --type "url" --options '{"title": "uitests"}'
```

You can visit ``127.0.0.1:5000``, or ``localhost:5000`` in a web browser to
see the redash login page.

___

#### Docker test

Build the redash-ui-tests with this command:

```text
docker build -t "redash-ui-tests:latest"
```

Then run the tests:

```text
docker run --net="host" --env REDASH_SERVER_URL=http://127.0.0.1:5000 redash-ui-tests:latest
```

If there are failures you can view the html report by first running this
command

```text
docker cp ui-tests:/home/user/src/report.html ./report.html
```

and open the ```report.html```, which should be located within the projects
root directory, in your web browser.

#### Using make

Redash-ui-tests include a Makefile to run setup and tests.

##### Make commands

To setup the redash instance us:e ```make setup-redash```.
To run the docker tests use: ```make docker-ui-tests```.
To run the tests using a local firefox browser use: ```make ui-tests```.

## Break a test

🚧 **TODO**

[ci]: https://circleci.com/gh/mozilla/redash-ui-tests/
[docker-compose-install]: https://docs.docker.com/compose/install/
[docker-compose]: https://docs.docker.com/compose/
[docker-install]: https://docs.docker.com/install/
[docker]: https://docs.docker.com/
[geckodriver]: https://github.com/mozilla/geckodriver/releases
[git-downloads]: https://git-scm.com/downloads
[git]: https://git-scm.com/
[github]: https://github.com/
[pipenv]: https://pipenv.readthedocs.io/en/latest/#install-pipenv-today
