# Markdown Code Block Converter

A Python tool that converts indented code blocks to fenced code blocks (triple backticks) in Markdown files.

## Features

- Processes all Markdown files (`.md`, `.markdown`, `.mdown`, `.mkd`) in a directory
- Detects indented code blocks (4+ spaces or 1+ tabs)
- **Preserves frontmatter** - Skips YAML (`---`) and TOML (`+++`) frontmatter sections
- Converts indented blocks to fenced code blocks with triple backticks
- Preserves original formatting and content
- Provides detailed processing feedback
- Includes dry-run mode for previewing changes

## Usage

### Basic Usage

Process all Markdown files in the current directory:
```bash
python md_codeblock_converter.py
```

Process files in a specific directory:
```bash
python md_codeblock_converter.py /path/to/markdown/files
```

### Dry Run Mode

Preview what changes would be made without modifying files:
```bash
python md_codeblock_converter.py --dry-run
python md_codeblock_converter.py /path/to/files --dry-run
```

### Command Line Options

- `directory` (optional): Directory containing markdown files (default: current directory)
- `--dry-run`: Preview changes without modifying files

## How It Works

The tool identifies indented code blocks by looking for:

1. Lines that start with 4 or more spaces
2. Lines that start with 1 or more tab characters
3. Empty lines within code blocks

It also recognizes and preserves frontmatter:

- YAML frontmatter delimited by `---`
- TOML frontmatter delimited by `+++`

The conversion process:

1. Detects and skips frontmatter sections
2. Identifies indented code blocks outside of frontmatter
3. Removes the indentation from each code block
4. Wraps the unindented code in triple backticks (```)
5. Replaces the original indented block in the file

## Example Conversion

**Before:**
```markdown
Here's some code:

    def hello_world():
        print("Hello, World!")
        return True

And here's more text.
```

**After:**
```markdown
Here's some code:

```
def hello_world():
    print("Hello, World!")
    return True
```

And here's more text.
```

## Frontmatter Example

**Before (with TOML frontmatter):**
```markdown
+++
title = "My Post"
draft = false
+++

# Content

Here's some code:

    def example():
        return "test"
```

**After:**
```markdown
+++
title = "My Post" 
draft = false
+++

# Content

Here's some code:

```
def example():
    return "test"
```
```

Notice how the frontmatter indentation is preserved while the code block is converted.

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Installation

1. Clone or download this repository
2. Make sure Python 3.6+ is installed
3. Run the script directly

## Error Handling

The tool includes comprehensive error handling for:
- Invalid directories
- File read/write permissions
- Encoding issues
- Unexpected file formats

## Output

The tool provides colored output showing:
- ✅ Successfully processed files
- ⏭️ Files that needed no changes  
- ❌ Files that encountered errors
- 📊 Summary statistics

## Safety

- The tool modifies files in-place
- Use `--dry-run` to preview changes first
- Consider backing up important files before running
- The tool only processes files with markdown extensions

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This project is open source and available under the MIT License.