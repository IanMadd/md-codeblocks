#!/usr/bin/env python3
"""
Example usage of the Markdown Code Block Converter

This script demonstrates how to use the MarkdownCodeBlockConverter class
in your own Python projects.
"""

from md_codeblock_converter import MarkdownCodeBlockConverter


def example_usage():
    """Demonstrate basic usage of the converter."""
    
    # Example 1: Convert files in current directory
    print("=== Example 1: Current Directory ===")
    try:
        converter = MarkdownCodeBlockConverter(".")
        results = converter.process_all_files()
        print(f"Processed {results['processed']} files successfully")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n")
    
    # Example 2: Convert files in a specific directory
    print("=== Example 2: Specific Directory ===")
    directory = "/path/to/your/markdown/files"  # Change this path
    try:
        converter = MarkdownCodeBlockConverter(directory)
        results = converter.process_all_files()
        print(f"Processed {results['processed']} files successfully")
    except ValueError as e:
        print(f"Directory not found: {e}")
    
    print("\n")
    
    # Example 3: Process a single file programmatically
    print("=== Example 3: Single File Processing ===")
    try:
        converter = MarkdownCodeBlockConverter(".")
        markdown_files = converter.find_markdown_files()
        
        if markdown_files:
            file_path = markdown_files[0]  # Process the first markdown file found
            was_modified = converter.process_file(file_path)
            if was_modified:
                print(f"✅ Modified: {file_path.name}")
            else:
                print(f"⏭️  No changes needed: {file_path.name}")
        else:
            print("No markdown files found")
    except (ValueError, FileNotFoundError, IOError) as e:
        print(f"Error processing file: {e}")
    
    print("\n")
    
    # Example 4: Just detect code blocks without converting
    print("=== Example 4: Detection Only ===")
    sample_content = """# Sample
    
Here's some code:

    def example():
        return "indented code"
        
And here's more text.
"""
    
    converter = MarkdownCodeBlockConverter(".")
    code_blocks = converter.detect_indented_code_blocks(sample_content)
    print(f"Found {len(code_blocks)} indented code blocks")
    
    for i, (start, end, content) in enumerate(code_blocks, 1):
        print(f"Block {i}: lines {start+1}-{end+1}")
        print(f"Content preview: {content[:50]}...")


if __name__ == "__main__":
    example_usage()