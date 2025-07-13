# Makefile for ash84.io static site

.PHONY: install format lint

# Install zvc package globally
install:
	pip install -e .

format: 
	ruff format .
	ruff check . --fix
 
lint:
	ruff check .