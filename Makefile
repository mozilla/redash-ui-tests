.DEFAULT_GOAL := help

REDASH_SERVER_URL = "http://127.0.0.1:5000/"
DOCKER_TAG = "redash-ui-tests"

.PHONY: clean
clean: ## Delete pyc files
	@find . -type f -name "*.pyc" -delete

.PHONY: build
build: ## Build Docker image
	@docker build -t "${DOCKER_TAG}" .

.PHONY: docker-ui-tests
docker-ui-tests: clean build ## Build and run tests in container
	@docker run \
		--net="host" \
		--env REDASH_SERVER_URL="${REDASH_SERVER_URL}" \
		--mount type=bind,source="${CURDIR}",target=/home/user/src \
		"${DOCKER_TAG}"

.PHONY: clean ui-tests
ui-tests: ## Run tests outside of container
	@pipenv run pytest

.PHONY: setup-redash
setup-redash: clean ## Setup redash instance
	@docker-compose run --rm server create_db
	@docker-compose run --rm postgres psql -h postgres -U postgres -c "create database tests"
	@docker-compose run --rm server /app/manage.py users create_root root@example.com "rootuser" --password "IAMROOT" --org default

.PHONY: bash
bash: ## Run bash in container as user
	@docker run -i -t --user user "${DOCKER_TAG}" /bin/bash

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
