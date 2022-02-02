CODE =\
	src \
	examples

TESTS =\
	tests

ALL = $(CODE)\
	$(TESTS)

VENV ?= .venv
JOBS ?= 4


init:
	test -d $(VENV) || python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install -U pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install

lint: black-lint flake8 mypy pytest-lint

black-lint:
	$(VENV)/bin/black --check $(CODE)

black-format:
	$(VENV)/bin/black $(CODE)

flake8:
	$(VENV)/bin/flake8 --statistics --jobs $(JOBS) --show-source $(ALL)

mypy:
	$(VENV)/bin/mypy --install-types --non-interactive $(CODE)

pytest-lint:
	$(VENV)/bin/pytest --dead-fixtures --dup-fixtures $(CODE)

pretty: black-format \
	$(VENV)/bin/isort $(ALL)

plint: pretty lint

precommit_install:
	@git init
	echo '#!/bin/sh\nmake lint\n' >> .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	$(VENV)/bin/pytest tests --cov=src --ignore=.DS_Store

coverage-report:
	$(VENV)/bin/coverage report -m

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf cover


doc:
	make -C docs html
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	make -C docs spelling