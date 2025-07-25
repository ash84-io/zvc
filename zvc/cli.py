import datetime
import os
import re
import shutil

import markdown
import typer
import yaml
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)

from zvc.config import Config

app = typer.Typer()
console = Console()


# Define a filter to clean HTML content
def clean_html(text: str) -> str:
    return re.sub(r"<.*?>", "", text)


# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("."))
env.filters["clean"] = clean_html


def extract_frontmatter(md_content):
    """Extract frontmatter from markdown content and return frontmatter dict and content without frontmatter."""
    lines = md_content.split("\n")

    # Check if the file starts with frontmatter (---)
    if lines and lines[0].strip() == "---":
        # Find the closing --- of the frontmatter
        frontmatter_lines = []
        content_start_idx = 0

        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                content_start_idx = i + 1
                break
            frontmatter_lines.append(line)

        # Extract frontmatter data
        frontmatter = {}
        for line in frontmatter_lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip("'\"").strip(",")
                frontmatter[key] = value

        # Return frontmatter and content without frontmatter
        content_without_frontmatter = "\n".join(lines[content_start_idx:])
        return frontmatter, content_without_frontmatter

    # If no frontmatter, return empty dict and original content
    return {}, md_content


def convert_markdown_to_html(
    config: Config,
    md_path: str,
    html_path: str,
    title=None,
):
    """Convert a markdown file to HTML using the theme template and save it to the specified path."""
    # Create directory if it doesn't exist
    dir_path = os.path.dirname(html_path)
    os.makedirs(dir_path, exist_ok=True)

    # Read markdown content
    with open(md_path, "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    # Extract frontmatter and get content without it
    frontmatter, content_without_frontmatter = extract_frontmatter(md_content)

    # Use title from frontmatter if available, otherwise use filename
    if not title and "title" in frontmatter:
        title = frontmatter["title"]
    else:
        title = os.path.basename(md_path).replace(".md", "")

    # Convert markdown to HTML
    html_content = markdown.markdown(
        content_without_frontmatter, extensions=["fenced_code", "tables", "nl2br"]
    )

    # Get theme from config
    template_path = f"themes/{config.theme.name}/post.html"

    # Create post data
    created_at = frontmatter.get(
        "pub_date", datetime.datetime.now().strftime("%Y-%m-%d")
    )
    url_path = dir_path
    post = {
        "title": title,
        "html": html_content,
        "created_at": created_at,
        "featured_image": frontmatter.get("featured_image", ""),
        "path": url_path,
        "description": frontmatter.get("description", ""),
    }

    # Get tags if available
    tag_list = []
    if "tags" in frontmatter:
        tags = frontmatter["tags"]
        if tags:
            # Remove extra quotes and brackets from the string representation
            cleaned_tags = tags.strip("[]'\"")
            tag_list = [tag.strip().strip("'\"") for tag in cleaned_tags.split(",")]

    # Set up template context
    context = {
        "post": post,
        "tag_list": tag_list,
        "settings": {
            "blog_title": title,
            "blog_desc": frontmatter.get("description", ""),
        },
    }

    try:
        # Render template
        template = env.get_template(template_path)
        rendered_html = template.render(**context)

        # Write HTML to file
        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(rendered_html)
    except Exception as e:
        raise e


def create_index_html(config: Config, post_list: list[dict]):
    """Create an index.html file in the docs directory using the theme's index template."""
    # Get theme from config
    template_path = f"themes/{config.theme.name}/index.html"

    # Make sure the docs directory exists
    os.makedirs(config.publication.path, exist_ok=True)

    # Set up template context
    context = {
        "post_list": post_list,
        "settings": {
            "blog_title": config.blog.title,
            "blog_desc": config.blog.description,
        },
    }

    try:
        # Render template
        template = env.get_template(template_path)
        rendered_html = template.render(**context)

        # Write HTML to file
        index_path = os.path.join("docs", "index.html")
        with open(index_path, "w", encoding="utf-8") as html_file:
            html_file.write(rendered_html)

        console.print(f"[green]Created index.html:[/green] {index_path}")
    except Exception as e:
        raise e


def clear_directory(directory):
    if os.path.exists(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        console.print(f"[green]Cleared directory:[/green] {directory}")
    else:
        os.makedirs(directory, exist_ok=True)
        console.print(f"[green]Created directory:[/green] {directory}")


def copy_theme_assets(config: Config):
    theme_assets_dir = os.path.join("themes", config.theme.name, "assets")
    docs_assets_dir = os.path.join(config.publication.path, "assets")

    if os.path.exists(theme_assets_dir):
        # Create docs assets directory if it doesn't exist
        os.makedirs(docs_assets_dir, exist_ok=True)

        # Copy all assets from theme to docs
        console.print(f"[green]Copying theme assets from:[/green] {theme_assets_dir}")

        # Walk through all files and directories in theme assets
        for root, dirs, files in os.walk(theme_assets_dir):
            # Calculate relative path from theme assets dir
            rel_path = os.path.relpath(root, theme_assets_dir)

            # Create corresponding directory in docs assets
            if rel_path != ".":
                target_dir = os.path.join(docs_assets_dir, rel_path)
                os.makedirs(target_dir, exist_ok=True)
            else:
                target_dir = docs_assets_dir

                # Copy all files
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)

        console.print(f"[green]Theme assets copied to:[/green] {docs_assets_dir}")
    else:
        console.print(f"[yellow]No theme assets found at:[/yellow] {theme_assets_dir}")


def copy_content_assets(source_dir, target_dir):
    """Copy all non-markdown files from source directory to target directory."""
    if not os.path.exists(source_dir):
        return

    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    # Get all files in the source directory
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        target_item = os.path.join(target_dir, item)

        # Skip markdown files
        if os.path.isfile(source_item) and not item.endswith(".md"):
            shutil.copy2(source_item, target_item)
            console.print(
                f"[green]Copied asset:[/green] {source_item} -> {target_item}"
            )


def get_all_markdown_files():
    """Get all markdown files in the contents directory."""
    md_files = []
    contents_dir = "contents"

    if os.path.exists(contents_dir):
        for root, dirs, files in os.walk(contents_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))

    return md_files


# Read config.yaml
def read_config():
    with open("config.yaml", "r", encoding="utf-8") as config_file:
        return Config.load(d=yaml.safe_load(config_file))


def get_date_path_from_frontmatter(frontmatter):
    """Extract date from frontmatter and return path components (year/month/day)."""
    date_str = frontmatter.get("pub_date", datetime.datetime.now().strftime("%Y-%m-%d"))

    try:
        # Try to parse the date string
        if "-" in date_str:
            # Format: YYYY-MM-DD
            date_parts = date_str.split("-")
            if len(date_parts) >= 3:
                year, month, day = date_parts[0], date_parts[1], date_parts[2]
                return year, month, day

        # If we couldn't parse it as YYYY-MM-DD, use current date
        today = datetime.datetime.now()
        return today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")

    except Exception:
        # If any error occurs, use current date
        today = datetime.datetime.now()
        return today.strftime("%Y"), today.strftime("%m"), today.strftime("%d")


@app.command()
def init():
    """Initialize the blog structure with required directories and config file."""
    console.print("[bold blue]Initializing blog structure...[/bold blue]")

    # Get the path to the initdir directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    initdir_path = os.path.join(current_dir, "initdir")

    # Copy config.yaml
    shutil.copy(os.path.join(initdir_path, "config.yaml"), "config.yaml")
    console.print("[green]Created file:[/green] config.yaml")

    # Copy contents directory
    contents_src = os.path.join(initdir_path, "contents")
    if os.path.exists(contents_src):
        shutil.copytree(contents_src, "contents", dirs_exist_ok=True)
        console.print("[green]Created directory:[/green] contents")

    # Copy themes directory
    themes_src = os.path.join(initdir_path, "themes")
    if os.path.exists(themes_src):
        shutil.copytree(themes_src, "themes", dirs_exist_ok=True)
        console.print("[green]Created directory:[/green] themes")

    # Create docs directory
    os.makedirs("docs", exist_ok=True)
    console.print("[green]Created directory:[/green] docs")

    console.print("[bold green]Initialization complete![/bold green]")
    console.print(
        "\nTo create your first post, add a markdown file to the 'contents' directory."
    )
    console.print("Then run 'zvc build' to generate your site.")


@app.command()
def clean():
    """Clean the generated files"""
    config: Config = read_config()
    console.print("[bold blue]Cleaning generated files...[/bold blue]")
    clear_directory(config.publication.path)
    console.print("[bold green]Cleaning complete![/bold green]")


@app.command()
def build():
    """Build the static site."""
    # Load configuration
    config: Config = read_config()

    console.print("[bold blue]Building static site...[/bold blue]")

    # Clear docs directory
    clear_directory("docs")

    # Copy theme assets
    copy_theme_assets(config=config)

    # Get all markdown files
    md_files = get_all_markdown_files()

    # Create post list for index.html
    post_list = []

    # Process each markdown file
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        task = progress.add_task(
            "[green]Converting markdown files...", total=len(md_files)
        )

        for md_file in md_files:
            # Read markdown content for frontmatter
            with open(md_file, "r", encoding="utf-8") as file:
                md_content = file.read()

            frontmatter, _ = extract_frontmatter(md_content)

            # Get title from frontmatter or filename
            title = frontmatter.get(
                "title", os.path.basename(md_file).replace(".md", "")
            )

            # Get date components from frontmatter
            year, month, day = get_date_path_from_frontmatter(frontmatter)

            # Determine HTML path with date-based structure
            rel_path = os.path.relpath(md_file, "contents")
            slug = os.path.basename(os.path.dirname(rel_path))

            # Create date-based path: docs/YYYY/MM/DD/slug/index.html
            html_dir = os.path.join("docs", year, month, day, slug)
            html_filename = "index.html"
            html_path = os.path.join(html_dir, html_filename)

            # Convert markdown to HTML
            convert_markdown_to_html(
                config=config, md_path=md_file, html_path=html_path
            )

            # Copy other files from the content directory to the output directory
            content_dir = os.path.dirname(md_file)
            copy_content_assets(content_dir, html_dir)

            # Add to post list with the new URL format
            post_url = f"/{year}/{month}/{day}/{slug}/"

            post_list.append(
                {
                    "title": title,
                    "link": post_url,
                    "pub_date": frontmatter.get(
                        "pub_date", datetime.datetime.now().strftime("%Y-%m-%d")
                    ),
                    "description": frontmatter.get("description", ""),
                }
            )

            progress.update(task, advance=1)
    # Sort post_list by pub_date in descending order (newest first)
    post_list.sort(key=lambda x: x["pub_date"], reverse=True)
    # Create index.html
    create_index_html(post_list=post_list, config=config)

    console.print("[bold green]Build complete![/bold green]")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
