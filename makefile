#
# System configuration
#
PYTHON=/usr/bin/python3

#
# You shouldn't need to touch anything below this line.
#
py_env=venv
py_packages=gutenberg_http
app_runner=$(py_env)/bin/python runserver.py

.PHONY: default
default: server

$(py_env)/bin/activate: requirements.txt
	if [ ! -d $(py_env) ]; then $(PYTHON) -m venv $(py_env); $(py_env)/bin/pip install -U pip setuptools; fi
	$(py_env)/bin/pip install -r requirements.txt
	test -f requirements-dev.txt && $(py_env)/bin/pip install -r requirements-dev.txt

venv: $(py_env)/bin/activate

unit-tests: venv
	$(py_env)/bin/nosetests --exe

tests: unit-tests

lint: venv
	$(py_env)/bin/flake8 $(py_packages)
	command -v shellcheck >/dev/null 2>&1 && shellcheck *.sh

typecheck: venv
	$(py_env)/bin/mypy --ignore-missing-imports --follow-imports=skip $(py_packages)

ci: tests lint typecheck

server: venv
	$(app_runner)
