.PHONY: environment
environment:  ## create environment
	pyenv install -s 3.9.19
	pyenv virtualenv 3.9.19 injectable
	pyenv local injectable

.PHONY: requirements
requirements:  ## install all requirements
	pip install ".[docs,test,build]"

.PHONY: flake-check
flake-check:  ## check PEP-8 and other standards with flake8
	@echo ""
	@echo "\033[33mFlake 8 Standards\033[0m"
	@echo "\033[33m=================\033[0m"
	@echo ""
	@python -m flake8 && echo "\n\n\033[32mSuccess\033[0m\n" || (echo \
	"\n\n\033[31mFailure\033[0m\n\n\033[34mManually fix the offending \
	issues\033[0m\n" && exit 1)

.PHONY: black-check
black-check:  ## check Black code style
	@echo ""
	@echo "\033[33mBlack Code Style\033[0m"
	@echo "\033[33m================\033[0m"
	@echo ""
	@python -m black --target-version=py39 --check --exclude="build/|buck-out/|dist/|_build/\
	|pip/|env/|\.pip/|\.git/|\.hg/|\.mypy_cache/|\.tox/|\.venv/" . \
	&& echo "\n\n\033[32mSuccess\033[0m\n" || (echo "\n\n\033[31mFailure\033[0m\n\n\
	\033[34mRun \"\e[4mmake black\e[24m\" to apply style formatting to your code\
	\033[0m\n" && exit 1)

.PHONY: black
black:  ## apply the Black code style to code
	black --target-version=py39 --exclude="build/|buck-out/|dist/|_build/|pip/|env/|\.pip/|\.git/\
	|\.hg/|\.mypy_cache/|\.tox/|\.venv/" .

.PHONY: tests
tests:  ## run tests with pytest
	pip install -e .[test]
	python -m pytest --cov=injectable --cov-report term --cov-report html:htmlcov \
	--cov-report xml:coverage.xml tests

.PHONY: unit-tests
unit-tests:  ## run unit tests with pytest
	pip install -e .[test]
	python -m pytest --cov=injectable --cov-report term --cov-report \
	html:tests/unit/htmlcov --cov-report xml:tests/unit/coverage.xml tests/unit

.PHONY: fixes-tests
fixes-tests:  ## run fixes tests with pytest
	pip install -e .[test]
	python -m pytest --cov=injectable --cov-report term --cov-report \
	html:tests/fixes/htmlcov --cov-report xml:tests/fixes/coverage.xml tests/fixes

.PHONY: examples-tests
examples-tests:  ## run examples tests with pytest
	pip install -e .[test]
	python -m pytest --cov=injectable --cov-report term --cov-report \
	html:tests/examples/htmlcov --cov-report xml:tests/examples/coverage.xml \
	tests/examples

.PHONY: checks
checks: black-check flake-check  ## perform code standards and style checks

.PHONY: package
package:
	pip install -e .[build]
	flit build

.PHONY: docs
docs:
	make html -B
	cp -a build/html/. docs

CURRENT_VERSION = 4.0.1

.PHONY: bump-patch-version
bump-patch-version:
	bump2version --allow-dirty --current-version $(CURRENT_VERSION) patch

.PHONY: bump-minor-version
bump-minor-version:
	bump2version --allow-dirty --current-version $(CURRENT_VERSION) minor

.PHONY: bump-major-version
bump-major-version:
	bump2version --allow-dirty --current-version $(CURRENT_VERSION) major

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs
BUILDDIR      = build

.PHONY: Makefile
# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: clean
clean:  ## delete all compiled python files
	find . -name "*.py[co]" -delete
	find . -name "*~" -delete
	find . -name "__pycache__" -delete

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
.PHONY: help
help:
	@echo "\n$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo
