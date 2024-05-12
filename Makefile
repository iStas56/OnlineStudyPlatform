# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = docker-compose.yml
DOCKER = docker
PYTHON = python
ALEMBIC = alembic
TEST_DIR = test/
HOST_PORT = 8000
CONTAINER_PORT = 8000
SERVICE = onlinecoursesplatform-web-1
DB_SERVICE = onlinecoursesplatform-db-1

# Database variables from .env
DB_USER = $(POSTGRES_USER)
DB_NAME = $(POSTGRES_DB)

# Docker commands
up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down

build:
	$(DOCKER_COMPOSE) build

restart:
	$(DOCKER_COMPOSE) restart

test:
	$(DOCKER) exec $(SERVICE) $(PYTHON) -m pytest $(TEST_DIR)

shell:
	$(DOCKER) exec -it $(SERVICE) /bin/bash

dbshell:
	$(DOCKER) exec -it $(DB_SERVICE) /bin/bash


# Default target
.DEFAULT_GOAL := help
