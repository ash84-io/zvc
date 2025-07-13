
![logo](logo.png)


[![Lint](https://github.com/ash84-io/zvc/actions/workflows/lint.yml/badge.svg)](https://github.com/ash84-io/zvc/actions/workflows/lint.yml)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/ash84/zv)

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
│ clean                                                                        │
│ build   Build the static site.                                               │
│ dev     Build the site and start a development server.                       │
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