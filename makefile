#
# System configuration
#
PYTHON=/usr/bin/python3

#
# You shouldn't need to touch anything below this line.
#
py_env=venv
py_packages=gutenberg_http
app_runner=$(py_env)/bin/python runserver

.PHONY: default
default: server

$(py_env)/bin/activate: requirements.txt
	test -d $(py_env) || $(PYTHON) -m venv $(py_env)
	$(py_env)/bin/pip install -r requirements.txt
	test -f requirements-dev.txt && $(py_env)/bin/pip install -r requirements-dev.txt

venv: $(py_env)/bin/activate

unit-tests: venv
	$(py_env)/bin/nosetests

tests: unit-tests

lint: venv
	$(py_env)/bin/flake8 $(py_packages)

typecheck: venv
	$(py_env)/bin/mypy --ignore-missing-imports --follow-imports=skip $(py_packages)

ci: tests lint typecheck

server: venv
	$(app_runner)
