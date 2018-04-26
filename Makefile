.DEFAULT_GOAL := help

REDASH_SERVER_URL = "http://127.0.0.1:5000/"
DOCKER_TAG = "redash-ui-tests"

.PHONY: clean
clean: ## Delete pyc files
	@find . -type f -name "*.pyc" -delete

.PHONY: build
build: ## Build Docker image
	@docker build -t "${DOCKER_TAG}" .

.PHONY: tests
tests: clean build ## Run tests in container
	@docker run \
		--net="host" \
		--env REDASH_SERVER_URL="${REDASH_SERVER_URL}" \
		--mount type=bind,source="${CURDIR}",target=/home/user/src \
		"${DOCKER_TAG}"

.PHONY: bash
bash: ## Run bash in container as user
	@docker run -i -t --user user "${DOCKER_TAG}" /bin/bash

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'
