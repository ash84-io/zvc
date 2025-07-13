# Makefile for ash84.io static site

.PHONY: install install-dev format lint build publish

# Install zvc package globally
install:
	pip3 install .

install-dev:
	pip3 install -e .

format: 
	ruff format .
	ruff check . --fix
 
lint:
	ruff check .

# Build package for PyPI
build:
	rm -rf dist
	python -m build

# Publish to PyPI
publish: build
	python -m twine upload dist/*

requirements:
	uv pip compile pyproject.toml -o requirements.txt
	uv pip compile pyproject.toml --extra dev -o requirements-dev.txt