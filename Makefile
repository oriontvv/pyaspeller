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

lint: ruff mypy

ruff:
	$(VENV)/bin/ruff .

mypy:
	$(VENV)/bin/mypy --install-types --non-interactive \
	--explicit-package-bases --namespace-packages --check-untyped-defs $(CODE)

pytest-lint:
	$(VENV)/bin/pytest --dead-fixtures --dup-fixtures $(CODE)

pretty:
	$(VENV)/bin/ruff --silent --exit-zero --fix .

plint: pretty lint

precommit_install:
	@git init
	echo '#!/bin/sh\nmake lint\n' >> .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	$(VENV)/bin/python -m pytest tests --cov=src --ignore=.DS_Store

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

build:
	$(VENV)/bin/poetry build

publish:
	$(VENV)/bin/poetry publish

doc:
	make -C docs html
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	make -C docs spelling