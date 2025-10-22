# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.7] - 2025-10-22

### Added
- Author field support in markdown frontmatter
- Author information is now displayed on both post pages and index page
- Author appears alongside publication date in format "· by {author}"
- Comprehensive test coverage for author field extraction
- Documentation for markdown frontmatter fields including author

### Changed
- Updated templates to render author information when available
- Enhanced post and post_list data structures to include author field

### Tests
- Added `test_extract_frontmatter_with_author` - validates author extraction
- Added `test_extract_frontmatter_without_author` - validates graceful handling of missing author
- Added `test_extract_frontmatter_no_frontmatter` - validates handling of content without frontmatter

## [0.1.6] - Previous Release

Initial stable release with core functionality.

