
![logo](https://github.com/ash84-io/zvc/raw/main/logo.png)


[![Lint](https://github.com/ash84-io/zvc/actions/workflows/lint.yml/badge.svg)](https://github.com/ash84-io/zvc/actions/workflows/lint.yml)
[![Version](https://img.shields.io/badge/version-0.1.6-blue.svg)](https://github.com/ash84/zvc)

---

# install 

```shell 
pip3 install zvc
```

# help 
```shell 
> zvc --help 

 Usage: zvc [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ init    Initialize the blog structure with required directories and config   │
│         file.                                                                │
│ clean   Clean the generated files                                            │
│ build   Build the static site.                                               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

# init 

```shell 
> mkdir blog 
> cd blog 
> zvc init 
Initializing blog structure...
Created directory: contents
Created directory: themes
Created directory: themes/default
Created directory: themes/default/assets
Created file: config.yaml
Created file: themes/default/index.html
Created file: themes/default/post.html
Created file: themes/default/assets/style.css
Created directory: docs
Initialization complete!
```


# build 

```shell 
> zvc build 
Building static site...
Cleared directory: docs
Copying theme assets from: themes/default/assets
Theme assets copied to: ./docs/assets
  Converting markdown files... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
Created index.html: docs/index.html
Build complete!
```

# run 

```shell 
> python -m http.server 8000  --directory ./docs 
```

![example](https://github.com/ash84-io/zvc/raw/main/example.png)

# Markdown Frontmatter

zvc supports frontmatter in markdown files. You can add metadata at the top of your markdown files using YAML format.

## Supported Fields

- `title`: Post title
- `author`: Post author (optional)
- `pub_date`: Publication date (YYYY-MM-DD format)
- `description`: Post description
- `featured_image`: URL to featured image
- `tags`: List of tags

## Example

```markdown
---
title: 'My First Post'
author: 'John Doe'
pub_date: '2024-07-13'
description: 'This is my first blog post'
featured_image: ''
tags: ['blog', 'tutorial']
---

# Your Content Here

Write your blog post content below the frontmatter.
```

The `author` field will be displayed in both the post page and the index page alongside the publication date.