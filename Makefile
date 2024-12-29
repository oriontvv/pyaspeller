CODE =\
	src \
	examples

TESTS =\
	tests

ALL = $(CODE)\
	$(TESTS)

JOBS ?= 4


init:
	uv sync

lint: ruff mypy

ruff:
	uv run ruff check $(CODE)

mypy:
	uv run mypy --install-types --non-interactive \
	--explicit-package-bases --namespace-packages --check-untyped-defs $(CODE)

pytest-lint:
	uv run pytest --dead-fixtures --dup-fixtures $(CODE)

pretty:
	uv run ruff format $(CODE)

plint: pretty lint

precommit_install:
	@git init
	echo '#!/bin/sh\nmake lint\n' >> .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

test:
	uv run pytest $(TESTS) --cov=src --ignore=.DS_Store

coverage-report:
	uv run coverage report -m

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
	uv build

publish:
	uv publish

doc:
	make -C docs html
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	make -C docs spelling
