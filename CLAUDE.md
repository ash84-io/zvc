# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZVC is a static blog generator written in Python. It converts Markdown files with YAML frontmatter into a static HTML blog. Published on PyPI as `zvc`.

## Commands

| Task | Command |
|------|---------|
| Install (dev) | `make install-dev` (editable mode) |
| Format | `make format` (ruff format + ruff check --fix) |
| Lint | `make lint` (ruff check) |
| Run tests | `pytest` |
| Run single test | `pytest tests/test_cli.py::test_name` |
| Build package | `make build` |
| Publish to PyPI | `make publish` |
| Generate lockfiles | `make requirements` (uses uv) |

## Architecture

**CLI entry point:** `zvc/cli.py` → `main()` via Typer. Three commands: `init`, `build`, `clean`.

**Build pipeline (`build` command):**
1. Reads `config.yaml` → validated by Pydantic models in `zvc/config.py`
2. Clears and recreates `docs/` output directory
3. Copies theme assets from `themes/{name}/assets/` → `docs/assets/`
4. Walks `contents/` for all `.md` files
5. For each markdown file: extracts YAML frontmatter (`extract_frontmatter`), converts to HTML via `markdown` library, renders through Jinja2 theme template (`post.html`)
6. Output path: `docs/YYYY/MM/DD/{slug}/index.html` (date from `pub_date` frontmatter)
7. Non-markdown files in content dirs are copied alongside as assets
8. Generates `docs/index.html` from `index.html` theme template with all posts sorted newest-first

**Config model** (`zvc/config.py`): `Config` aggregates `BlogConfig` (title, description), `ThemeConfig` (name), `PublicationConfig` (path). All use Pydantic with `@classmethod load()` factory.

**Templates:** Jinja2 with `FileSystemLoader(".")`. Templates live at `themes/{name}/post.html` and `themes/{name}/index.html`. Custom `clean` filter strips HTML tags.

**Init scaffolding:** `zvc/initdir/` contains default config.yaml, sample content, and the default theme. Copied to CWD on `zvc init`.

## Frontmatter Format

```yaml
---
title: 'Post Title'
pub_date: 'YYYY-MM-DD'
description: 'Short description'
author: 'Author Name'           # optional
featured_image: 'url/to/image'  # optional
tags: ['tag1', 'tag2']          # optional
---
```

## Key Details

- Python 3.12+ required
- Frontmatter parsing is custom (not using `python-frontmatter`); see `extract_frontmatter()` in `cli.py`
- Markdown extensions enabled: `fenced_code`, `tables`, `nl2br`
- The `docs/` directory is the build output (suitable for GitHub Pages)
- CI runs lint on all branches/PRs; deploy workflow triggers on semver tags
