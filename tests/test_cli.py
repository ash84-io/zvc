from zvc.cli import extract_frontmatter


def test_extract_frontmatter_with_author():
    """Test that extract_frontmatter correctly extracts author from frontmatter."""
    md_content = """---
title: 'Test Post'
author: 'John Doe'
pub_date: '2024-07-13'
description: 'Test description'
tags: ['test', 'example']
---

# Test Content

This is a test post.
"""
    frontmatter, content = extract_frontmatter(md_content)

    assert frontmatter["title"] == "Test Post"
    assert frontmatter["author"] == "John Doe"
    assert frontmatter["pub_date"] == "2024-07-13"
    assert frontmatter["description"] == "Test description"
    assert "Test Content" in content


def test_extract_frontmatter_without_author():
    """Test that extract_frontmatter works when author is not present."""
    md_content = """---
title: 'Test Post Without Author'
pub_date: '2024-07-13'
---

# Test Content

This is a test post without author.
"""
    frontmatter, content = extract_frontmatter(md_content)

    assert frontmatter["title"] == "Test Post Without Author"
    assert "author" not in frontmatter
    assert "Test Content" in content


def test_extract_frontmatter_no_frontmatter():
    """Test that extract_frontmatter handles content without frontmatter."""
    md_content = """# Just a Title

Regular content without frontmatter.
"""
    frontmatter, content = extract_frontmatter(md_content)

    assert frontmatter == {}
    assert "Just a Title" in content
