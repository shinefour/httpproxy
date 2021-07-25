APP_NAME=htmlproxy
HTTP_PORT ?= 8080

.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build the container
	docker build -t $(APP_NAME) .

run: ## Run the app. Add HTTP_PORT=<PORT> to overwrite default (8080)
	export HTTP_PORT=${HTTP_PORT}
	docker-compose up