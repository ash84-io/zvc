import os
import shutil
import pytest
from typer.testing import CliRunner
from zvc.cli import (
    extract_frontmatter,
    convert_markdown_to_html,
    clear_directory,
    read_config,
    app,
)

# Fixture for temporary test directory
@pytest.fixture
def temp_test_dir(tmp_path):
    # Create test directory structure
    test_dir = tmp_path / "test_zvc"
    test_dir.mkdir()
    
    # Create necessary subdirectories
    (test_dir / "contents").mkdir()
    (test_dir / "themes" / "default" / "assets").mkdir(parents=True)
    (test_dir / "docs").mkdir()
    
    # Change to test directory
    original_dir = os.getcwd()
    os.chdir(test_dir)
    
    yield test_dir
    
    # Cleanup
    os.chdir(original_dir)
    shutil.rmtree(test_dir)

# Test frontmatter extraction
def test_extract_frontmatter():
    md_content = """---
title: Test Post
pub_date: 2024-01-01
tags: [test, blog]
---
# Test Content
This is a test post."""
    
    frontmatter, content = extract_frontmatter(md_content)
    
    assert frontmatter["title"] == "Test Post"
    assert frontmatter["pub_date"] == "2024-01-01"
    assert frontmatter["tags"] == "[test, blog]"
    assert content.startswith("# Test Content")

# Test markdown to HTML conversion
def test_convert_markdown_to_html(temp_test_dir):
    # Create test theme template
    template_dir = temp_test_dir / "themes" / "default"
    with open(template_dir / "post.html", "w") as f:
        f.write("{{ post.html }}")
    
    # Create test markdown file
    md_content = "# Test Heading\nTest content"
    md_path = temp_test_dir / "test.md"
    with open(md_path, "w") as f:
        f.write(md_content)
    
    # Create test config
    config_content = """
blog:
  title: Test Blog
  description: Test Description
theme:
  name: default
publication:
  path: docs
"""
    with open(temp_test_dir / "config.yaml", "w") as f:
        f.write(config_content)
    
    config = read_config()
    html_path = temp_test_dir / "docs" / "test.html"
    
    convert_markdown_to_html(config, str(md_path), str(html_path))
    
    assert html_path.exists()
    with open(html_path) as f:
        content = f.read()
        assert "<h1>Test Heading</h1>" in content
        assert "Test content" in content

# Test directory clearing
def test_clear_directory(temp_test_dir):
    test_dir = temp_test_dir / "test_clear"
    test_dir.mkdir()
    
    # Create some test files and directories
    (test_dir / "test_file.txt").write_text("test")
    (test_dir / "test_subdir").mkdir()
    
    clear_directory(str(test_dir))
    
    assert os.path.exists(test_dir)
    assert len(os.listdir(test_dir)) == 0

# Test CLI commands
def test_cli_init():
    runner = CliRunner()
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0

def test_cli_clean():
    runner = CliRunner()
    result = runner.invoke(app, ["clean"])
    assert result.exit_code == 0

def test_cli_build(temp_test_dir):
    # Create minimal test environment
    config_content = """
blog:
  title: Test Blog
  description: Test Description
theme:
  name: default
publication:
  path: docs
"""
    with open(temp_test_dir / "config.yaml", "w") as f:
        f.write(config_content)
    
    # Create test post
    post_dir = temp_test_dir / "contents" / "test-post"
    post_dir.mkdir(parents=True)
    with open(post_dir / "test-post.md", "w") as f:
        f.write("# Test Post\nTest content")
    
    # Create theme templates
    theme_dir = temp_test_dir / "themes" / "default"
    with open(theme_dir / "post.html", "w") as f:
        f.write("{{ post.html }}")
    with open(theme_dir / "index.html", "w") as f:
        f.write("{% for post in post_list %}{{ post.title }}{% endfor %}")
    
    runner = CliRunner()
    result = runner.invoke(app, ["build"])
    assert result.exit_code == 0
    assert (temp_test_dir / "docs" / "index.html").exists()