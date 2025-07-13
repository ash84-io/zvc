# Makefile for ash84.io static site

.PHONY: install format lint

# Install zv package globally
install:
	pipx install -e --force .

format: 
	ruff format .
	ruff check . --fix
 
lint:
	ruff check .