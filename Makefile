.DEFAULT_GOAL := help

REDASH_SERVER_URL = "http://127.0.0.1:5000/"
DOCKER_NAME ?= "redash-ui-tests"
DOCKER_TAG ?= "latest"

.PHONY: clean
clean: ## Delete pyc files
	@find . -type f -name "*.pyc" -delete

.PHONY: build
build: clean ## Build Docker image
	@docker build -t "${DOCKER_NAME}:${DOCKER_TAG}" .

.PHONY: docker-ui-tests
docker-ui-tests: clean ## Run tests in container and copy report.html
	@docker run \
		--net="host" \
		--name "redash-ui-tests" \
		--env REDASH_SERVER_URL="${REDASH_SERVER_URL}" \
		"${DOCKER_NAME}:${DOCKER_TAG}"
	@docker cp redash-ui-tests:/home/user/src/report.html ./report.html

.PHONY: ui-tests
ui-tests: clean ## Run tests outside of container
	@pipenv run pytest

.PHONY: flake8
flake8: clean ## Run flake8
	@pipenv run flake8

.PHONY: formatting
formatting: clean ## Run python black and show diff
	@pipenv run black --diff --check --line-length 88 ./

.PHONY: mypy
mypy: clean ## Run mypy
	@pipenv run mypy .

.PHONY: setup-redash
setup-redash: clean ## Setup redash instance
	@docker-compose run --rm server create_db
	@docker-compose run \
		--rm postgres psql \
		-h postgres \
		-U postgres \
		-c "create database tests"
	@docker-compose run \
		--rm server /app/manage.py users create_root \
		root@example.com \
		"rootuser" \
		--password "IAMROOT" \
		--org default
	@docker-compose run \
		--rm server /app/manage.py ds new \
		"ui-tests" \
		--type "url" \
		--options '{"title": "uitests"}'

.PHONY: bash
bash: ## Run bash in container as user
	@docker run -i -t --user user "${DOCKER_NAME}:${DOCKER_TAG}" /bin/bash

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
