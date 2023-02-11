BLACK ?= \033[0;30m
RED ?= \033[0;31m
GREEN ?= \033[0;32m
YELLOW ?= \033[0;33m
BLUE ?= \033[0;34m
PURPLE ?= \033[0;35m
CYAN ?= \033[0;36m
GRAY ?= \033[0;37m
WHITE ?= \033[1;37m
COFF ?= \033[0m

.PHONY: all shell build  migrate quality setup superuser runserver makemigrations lint-django lint-django-fix format

all: help

help:
	@echo -e "\n$(WHITE)Available commands:$(COFF)"
	@echo -e "$(CYAN)make setup$(COFF)            - Sets up the project in your local machine."
	@echo -e "                        This includes building Docker containers and running migrations."
	@echo -e "$(CYAN)make runserver$(COFF)        - Runs the django app in the container, available at http://127.0.0.1:8000"
	@echo -e "$(CYAN)make migrate$(COFF)          - Runs django's migrate command in the container"
	@echo -e "$(CYAN)make makemigrations$(COFF)   - Runs django's makemigrations command in the container"
	@echo -e "$(CYAN)make superuser$(COFF)        - Runs django's createsuperuser command in the container"
	@echo -e "$(CYAN)make shell$(COFF)            - Starts a Linux shell (bash) in the django container"


shell:
	@echo -e "$(CYAN)Starting Bash in the django container:$(COFF)"
	@docker-compose run --rm django bash


init-db:
	@echo -e "$(CYAN)Starting Bash in the postgres container:$(COFF)"
	@docker exec -it mail_service_db bash -c "psql -U postgres -c 'CREATE DATABASE shipdb;'"

build:
	@echo -e "$(CYAN)Creating Docker images:$(COFF)"
	@docker-compose build

runserver:
	@echo -e "$(CYAN)Starting Docker container with the app.$(COFF)"
	@docker-compose up
	@echo -e "$(CYAN)App ready and listening at http://127.0.0.1:8000.$(COFF)"

setup: build runserver init-db migrate
	@echo -e "$(GREEN)===================================================================="
	@echo "SETUP SUCCEEDED"
	@echo -e "Run 'make runserver' to start the Django development server.$(COFF)"

makemigrations:
	@echo -e "$(CYAN)Running django makemigrations:$(COFF)"
	@docker-compose run --rm django ./manage.py makemigrations $(cmd)

migrate:
	@echo -e "$(CYAN)Running django migrations:$(COFF)"
	@docker-compose run --rm django ./manage.py migrate $(cmd)

superuser:
	@echo -e "$(CYAN)Creating Docker images:$(COFF)"
	@docker-compose run --rm django ./manage.py createsuperuser

down:
	@docker-compose down

down-v:
	@docker-compose down --volume

lint-django:
	@echo -e "$(CYAN)Running Black check:$(COFF)"
	@docker-compose run --rm django black --check .

lint-django-fix:
	@echo -e "$(CYAN)Running Black formatting:$(COFF)"
	@docker-compose run --rm django black .
