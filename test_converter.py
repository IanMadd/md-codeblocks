#!/usr/bin/env python3
"""
Tests for the Markdown Code Block Converter

This module contains unit tests for the MarkdownCodeBlockConverter class.
"""

import unittest
import tempfile
from pathlib import Path
from md_codeblock_converter import MarkdownCodeBlockConverter


class TestMarkdownCodeBlockConverter(unittest.TestCase):
    """Test cases for MarkdownCodeBlockConverter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.converter = MarkdownCodeBlockConverter(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename: str, content: str) -> Path:
        """Helper method to create a test markdown file."""
        file_path = Path(self.temp_dir) / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_find_markdown_files(self):
        """Test finding markdown files in directory."""
        # Create test files
        self.create_test_file('test1.md', 'content')
        self.create_test_file('test2.markdown', 'content')
        self.create_test_file('test3.txt', 'content')  # Should be ignored
        self.create_test_file('test4.mdown', 'content')
        
        markdown_files = self.converter.find_markdown_files()
        
        self.assertEqual(len(markdown_files), 3)
        filenames = [f.name for f in markdown_files]
        self.assertIn('test1.md', filenames)
        self.assertIn('test2.markdown', filenames)
        self.assertIn('test4.mdown', filenames)
        self.assertNotIn('test3.txt', filenames)
    
    def test_detect_indented_code_blocks_simple(self):
        """Test detecting simple indented code blocks."""
        content = """# Title

Here's some text.

    def hello():
        print("Hello")
        return True

More text here."""
        
        code_blocks = self.converter.detect_indented_code_blocks(content)
        
        self.assertEqual(len(code_blocks), 1)
        start_line, end_line, code_content = code_blocks[0]
        self.assertEqual(start_line, 4)
        self.assertEqual(end_line, 6)
        self.assertIn('def hello():', code_content)
    
    def test_detect_multiple_code_blocks(self):
        """Test detecting multiple indented code blocks."""
        content = """# Title

First block:

    print("First")

Some text.

    print("Second")
    x = 1

End."""
        
        code_blocks = self.converter.detect_indented_code_blocks(content)
        
        self.assertEqual(len(code_blocks), 2)
        self.assertIn('First', code_blocks[0][2])
        self.assertIn('Second', code_blocks[1][2])
    
    def test_unindent_code_spaces(self):
        """Test unindenting code with spaces."""
        code_content = "    def test():\n        return True\n    # comment"
        result = self.converter.unindent_code(code_content)
        expected = "def test():\n    return True\n# comment"
        self.assertEqual(result, expected)
    
    def test_unindent_code_tabs(self):
        """Test unindenting code with tabs."""
        code_content = "\tdef test():\n\t\treturn True\n\t# comment"
        result = self.converter.unindent_code(code_content)
        expected = "def test():\n\treturn True\n# comment"
        self.assertEqual(result, expected)
    
    def test_convert_to_fenced_blocks_simple(self):
        """Test converting simple indented block to fenced."""
        content = """# Title

    def hello():
        print("Hello")

Text after."""
        
        result = self.converter.convert_to_fenced_blocks(content)
        
        self.assertIn('```', result)
        self.assertIn('def hello():', result)
        self.assertNotIn('    def hello():', result)  # Should be unindented
    
    def test_convert_no_indented_blocks(self):
        """Test content with no indented blocks remains unchanged."""
        content = """# Title

This is regular text.

```python
def existing_fenced():
    pass
```

More text."""
        
        result = self.converter.convert_to_fenced_blocks(content)
        self.assertEqual(content, result)
    
    def test_process_file_with_changes(self):
        """Test processing a file that needs changes."""
        content = """# Test

    def example():
        return "test"
"""
        file_path = self.create_test_file('test.md', content)
        
        result = self.converter.process_file(file_path)
        
        self.assertTrue(result)  # File was modified
        
        # Read the modified file
        with open(file_path, 'r', encoding='utf-8') as f:
            modified_content = f.read()
        
        self.assertIn('```', modified_content)
        self.assertNotIn('    def example():', modified_content)
    
    def test_process_file_no_changes(self):
        """Test processing a file that needs no changes."""
        content = """# Test

This is regular markdown with no indented code blocks.

```python
def already_fenced():
    pass
```
"""
        file_path = self.create_test_file('test.md', content)
        
        result = self.converter.process_file(file_path)
        
        self.assertFalse(result)  # File was not modified
    
    def test_process_all_files(self):
        """Test processing all files in directory."""
        # Create test files
        self.create_test_file('test1.md', """# Test 1

    def code1():
        pass
""")
        
        self.create_test_file('test2.md', """# Test 2

Regular content only.
""")
        
        self.create_test_file('test3.markdown', """# Test 3

    print("test")
""")
        
        results = self.converter.process_all_files()
        
        self.assertEqual(results['total'], 3)
        self.assertEqual(results['processed'], 2)  # test1.md and test3.markdown
        self.assertEqual(results['errors'], 0)
    
    def test_empty_directory(self):
        """Test processing empty directory."""
        empty_dir = tempfile.mkdtemp()
        converter = MarkdownCodeBlockConverter(empty_dir)
        
        results = converter.process_all_files()
        
        self.assertEqual(results['total'], 0)
        self.assertEqual(results['processed'], 0)
        self.assertEqual(results['errors'], 0)
        
        # Cleanup
        import shutil
        shutil.rmtree(empty_dir)
    
    def test_invalid_directory(self):
        """Test error handling for invalid directory."""
        with self.assertRaises(ValueError):
            MarkdownCodeBlockConverter('/nonexistent/directory')
    
    def test_complex_indented_block(self):
        """Test handling complex indented block with mixed content."""
        content = """# Example

Here's a complex example:

    # This is a comment
    def complex_function(param1, param2):
        \"\"\"
        A docstring with multiple lines
        \"\"\"
        if param1:
            result = []
            for item in param2:
                result.append(item.upper())
            return result
        return None

    # Another comment
    x = complex_function("test", ["a", "b"])

That was the code block."""
        
        result = self.converter.convert_to_fenced_blocks(content)
        
        # Should have fenced block
        self.assertIn('```', result)
        # Should not have the original indentation
        self.assertNotIn('    def complex_function', result)
        # But should preserve internal indentation
        lines = result.split('\n')
        code_section = False
        for line in lines:
            if line.strip() == '```' and not code_section:
                code_section = True
            elif line.strip() == '```' and code_section:
                code_section = False
            elif code_section and 'if param1:' in line:
                # This line should not be indented at the markdown level but should have Python indentation
                self.assertTrue(line.startswith('    ') or not line.startswith(' '))
    
    def test_frontmatter_toml_plus(self):
        """Test that TOML frontmatter with +++ delimiters is preserved."""
        content = """+++
title = "docker_plugin resource"
draft = false

platform = "linux"

[menu.resources]
    title = "docker_plugin"
    identifier = "resources/core/docker_plugin.md"
    parent = "resources/core"
+++

# Main Content

Here's some code:

    def example():
        return "test"
        
More content."""
        
        result = self.converter.convert_to_fenced_blocks(content)
        
        # Frontmatter should be preserved exactly
        self.assertTrue(result.startswith('+++'))
        self.assertIn('title = "docker_plugin resource"', result)
        self.assertIn('    title = "docker_plugin"', result)  # Indented TOML should remain
        self.assertIn('+++\n\n# Main Content', result)
        
        # Code block should be converted
        self.assertIn('```', result)
        self.assertNotIn('    def example():', result)  # Should be unindented
        self.assertIn('def example():', result)  # But should exist unindented
    
    def test_frontmatter_yaml(self):
        """Test that YAML frontmatter with --- delimiters is preserved."""
        content = """---
title: "Example Post"
date: 2023-01-01
tags:
  - python
  - markdown
categories:
    - development
---

# Content

Some indented code:

    print("Hello World")
    x = 1

End of content."""
        
        result = self.converter.convert_to_fenced_blocks(content)
        
        # Frontmatter should be preserved
        self.assertTrue(result.startswith('---'))
        self.assertIn('title: "Example Post"', result)
        self.assertIn('  - python', result)  # Indented YAML should remain
        self.assertIn('    - development', result)  # Different indentation should remain
        
        # Code block should be converted
        self.assertIn('```', result)
        self.assertNotIn('    print("Hello World")', result)
        self.assertIn('print("Hello World")', result)
    
    def test_frontmatter_no_code_blocks(self):
        """Test frontmatter with no code blocks remains unchanged."""
        content = """+++
title = "Simple Page"
+++

# Simple Content

Just regular text here.
No code blocks at all."""
        
        result = self.converter.convert_to_fenced_blocks(content)
        
        # Content should be completely unchanged
        self.assertEqual(content, result)
    
    def test_detect_frontmatter_boundaries(self):
        """Test the frontmatter boundary detection."""
        # Test TOML frontmatter
        toml_content = """+++
title = "Test"
    nested = "value"
+++

Content here"""
        start, end = self.converter.detect_frontmatter_boundaries(toml_content)
        self.assertEqual(start, 0)
        self.assertEqual(end, 3)  # Line with closing +++
        
        # Test YAML frontmatter
        yaml_content = """---
title: Test
  nested: value
---

Content here"""
        start, end = self.converter.detect_frontmatter_boundaries(yaml_content)
        self.assertEqual(start, 0)
        self.assertEqual(end, 3)  # Line with closing ---
        
        # Test no frontmatter
        no_fm_content = """# Regular Content

No frontmatter here"""
        start, end = self.converter.detect_frontmatter_boundaries(no_fm_content)
        self.assertIsNone(start)
        self.assertIsNone(end)


if __name__ == '__main__':
    unittest.main()