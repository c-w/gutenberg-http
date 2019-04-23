py_env=venv

.PHONY: default
default: server

requirements.txt.out: requirements.txt requirements-dev.txt
	if [ ! -d $(py_env) ]; then python3 -m venv $(py_env); $(py_env)/bin/pip install -U pip setuptools; fi
	$(py_env)/bin/pip install -r requirements.txt
	$(py_env)/bin/pip install -r requirements-dev.txt
	touch $(py_env)/requirements.txt.out

venv: requirements.txt.out

unit-tests: venv
	$(py_env)/bin/nose2 -v

tests: unit-tests

lint: venv
	$(py_env)/bin/flake8 gutenberg_http

typecheck: venv
	$(py_env)/bin/mypy --ignore-missing-imports --follow-imports=skip gutenberg_http

ci: tests lint typecheck

server: venv
	$(py_env)/bin/python runserver.py
