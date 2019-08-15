help: ## show this help
	@echo 'usage: make [target] ...'
	@echo ''
	@echo 'targets:'
	@egrep '^(.+)\:\ .*##\ (.+)' ${MAKEFILE_LIST} | sed 's/:.*##/#/' | column -t -c 2 -s '#'

env:  ## create python env
	virtualenv -p ~/.pyenv/versions/3.7.4/bin/python env

install:  ## install requirements
	env/bin/pip install -r requirements.txt

lint:  ## run flake8 and mypy linters
	env/bin/flake8 app tests
	env/bin/mypy --ignore-missing-imports --follow-imports=silent app

test: ## run tests with pytest
	docker-compose up -d mongo
	env/bin/pytest --cov=app tests

run: ## run in local
	docker-compose up -d mongo
	PORT=8080 env/bin/watchmedo auto-restart -d app -p '*.py' -- env/bin/python -m app.main

run_in_docker: ## run in docker
	docker-compose build
	docker-compose up -d
