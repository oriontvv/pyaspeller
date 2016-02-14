# Some simple testing tasks (sorry, UNIX only).

FLAGS=


flake:
#	python setup.py check -rms
	flake8 pyaspeller tests examples

develop:
	python setup.py develop

test: flake develop
	py.test tests --ignore=.DS_Store

vtest: flake develop
	py.test tests -v --ignore=.DS_Store


cov cover coverage: flake
	py.test tests --cov=pyaspeller --ignore=.DS_Store

package: cov
	python setup.py sdist bdist_wheel

publish: package
	python setup.py sdist bdist_wheel upload

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
	make -C docs clean
	python setup.py clean
	rm -rf .tox

doc:
	make -C docs html
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	make -C docs spelling

env:
	$(source ./py3/bin/activate)


.PHONY: all build env flake test vtest cov clean doc
