#!/usr/bin/env python3
"""
Markdown Code Block Converter

This script processes markdown files in a directory to convert indented code blocks 
to fenced code blocks (wrapped in tick marks).

Author: Generated Code
Date: September 25, 2025
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Tuple


class MarkdownCodeBlockConverter:
    """
    A class to handle the conversion of indented code blocks to fenced code blocks
    in markdown files.
    """
    
    def __init__(self, directory: str):
        """
        Initialize the converter with a target directory.
        
        Args:
            directory (str): Path to the directory containing markdown files
        """
        self.directory = Path(directory)
        if not self.directory.exists():
            raise ValueError(f"Directory {directory} does not exist")
        if not self.directory.is_dir():
            raise ValueError(f"{directory} is not a directory")
    
    def find_markdown_files(self) -> List[Path]:
        """
        Find all markdown files in the directory.
        
        Returns:
            List[Path]: List of paths to markdown files
        """
        markdown_extensions = ['.md', '.markdown', '.mdown', '.mkd']
        markdown_files = []
        
        for file in self.directory.iterdir():
            if file.is_file() and file.suffix.lower() in markdown_extensions:
                markdown_files.append(file)
        
        return sorted(markdown_files)
    
    def detect_frontmatter_boundaries(self, content: str) -> Tuple[int, int]:
        """
        Detect the boundaries of frontmatter in markdown content.
        
        Args:
            content (str): The markdown content as a string
            
        Returns:
            Tuple[int, int]: (start_line, end_line) of frontmatter, or (None, None) if no frontmatter
        """
        lines = content.split('\n')
        
        if not lines:
            return None, None
        
        # Check for TOML frontmatter (delimited by +++)
        if lines[0].strip() == '+++':
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '+++':
                    return 0, i
        
        # Check for YAML frontmatter (delimited by ---)
        elif lines[0].strip() == '---':
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    return 0, i
        
        return None, None
    
    def detect_indented_code_blocks(self, content: str) -> List[Tuple[int, int, str]]:
        """
        Detect indented code blocks in markdown content.
        
        Args:
            content (str): The markdown content as a string
            
        Returns:
            List[Tuple[int, int, str]]: List of tuples containing (start_line, end_line, code_content)
        """
        lines = content.split('\n')
        code_blocks = []
        current_block_start = None
        current_block_lines = []
        in_fenced_block = False
        
        # Detect frontmatter boundaries to skip them
        frontmatter_start, frontmatter_end = self.detect_frontmatter_boundaries(content)
        
        for i, line in enumerate(lines):
            # Skip frontmatter section
            if frontmatter_start is not None and frontmatter_start <= i <= frontmatter_end:
                continue
                
            # Check if we're entering or leaving a fenced code block
            if re.match(r'^```', line.strip()):
                in_fenced_block = not in_fenced_block
                # If we were in an indented block, end it now
                if current_block_start is not None:
                    current_block_start = None
                    current_block_lines = []
                continue
            
            # Skip processing if we're inside a fenced code block
            if in_fenced_block:
                continue
            
            # Check if line is indented with 4+ spaces or 1+ tabs (standard markdown code block)
            if re.match(r'^(    |\t+)', line) or (line.strip() == '' and current_block_start is not None):
                if current_block_start is None:
                    # Start of a new code block
                    current_block_start = i
                    current_block_lines = [line]
                else:
                    # Continue current code block
                    current_block_lines.append(line)
            else:
                # End of code block if we were in one
                if current_block_start is not None:
                    # Remove trailing empty lines
                    while current_block_lines and current_block_lines[-1].strip() == '':
                        current_block_lines.pop()
                    
                    if current_block_lines:  # Only add if there's actual content
                        code_blocks.append((current_block_start, current_block_start + len(current_block_lines) - 1, 
                                          '\n'.join(current_block_lines)))
                    current_block_start = None
                    current_block_lines = []
        
        # Handle case where file ends with a code block
        if current_block_start is not None and not in_fenced_block:
            while current_block_lines and current_block_lines[-1].strip() == '':
                current_block_lines.pop()
            if current_block_lines:
                code_blocks.append((current_block_start, current_block_start + len(current_block_lines) - 1,
                                  '\n'.join(current_block_lines)))
        
        return code_blocks
    
    def unindent_code(self, code_content: str) -> str:
        """
        Remove the indentation from code content.
        
        Args:
            code_content (str): The indented code content
            
        Returns:
            str: The unindented code content
        """
        lines = code_content.split('\n')
        unindented_lines = []
        
        for line in lines:
            # Remove 4 spaces or 1 tab from the beginning
            if line.startswith('    '):
                unindented_lines.append(line[4:])
            elif line.startswith('\t'):
                unindented_lines.append(line[1:])
            else:
                # For lines that might be empty or have less indentation
                unindented_lines.append(line)
        
        return '\n'.join(unindented_lines)
    
    def convert_to_fenced_blocks(self, content: str) -> str:
        """
        Convert indented code blocks to fenced code blocks.
        
        Args:
            content (str): The original markdown content
            
        Returns:
            str: The converted markdown content
        """
        lines = content.split('\n')
        code_blocks = self.detect_indented_code_blocks(content)
        
        if not code_blocks:
            return content
        
        # Process from end to beginning to avoid index shifting issues
        for start_line, end_line, code_content in reversed(code_blocks):
            # Unindent the code
            unindented_code = self.unindent_code(code_content)
            
            # Create fenced code block
            fenced_block = ['```'] + unindented_code.split('\n') + ['```']
            
            # Replace the original indented block with fenced block
            lines[start_line:end_line + 1] = fenced_block
        
        return '\n'.join(lines)
    
    def process_file(self, file_path: Path) -> bool:
        """
        Process a single markdown file.
        
        Args:
            file_path (Path): Path to the markdown file
            
        Returns:
            bool: True if file was modified, False otherwise
        """
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Convert indented blocks to fenced blocks
            converted_content = self.convert_to_fenced_blocks(original_content)
            
            # Check if content was actually changed
            if original_content != converted_content:
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(converted_content)
                print(f"✅ Processed: {file_path.name}")
                return True
            else:
                print(f"⏭️  No changes needed: {file_path.name}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
            return False
    
    def process_all_files(self) -> dict:
        """
        Process all markdown files in the directory.
        
        Returns:
            dict: Statistics about the processing results
        """
        markdown_files = self.find_markdown_files()
        
        if not markdown_files:
            print("No markdown files found in the directory.")
            return {"total": 0, "processed": 0, "errors": 0}
        
        print(f"Found {len(markdown_files)} markdown file(s) to process:\n")
        
        processed_count = 0
        error_count = 0
        
        for file_path in markdown_files:
            try:
                if self.process_file(file_path):
                    processed_count += 1
            except Exception as e:
                print(f"❌ Failed to process {file_path.name}: {str(e)}")
                error_count += 1
        
        results = {
            "total": len(markdown_files),
            "processed": processed_count,
            "errors": error_count
        }
        
        print(f"\n📊 Summary:")
        print(f"   Total files: {results['total']}")
        print(f"   Files modified: {results['processed']}")
        print(f"   Files with errors: {results['errors']}")
        print(f"   Files unchanged: {results['total'] - results['processed'] - results['errors']}")
        
        return results


def main():
    """
    Main function to run the markdown code block converter.
    """
    parser = argparse.ArgumentParser(
        description="Convert indented code blocks to fenced code blocks in markdown files"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory containing markdown files (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    
    args = parser.parse_args()
    
    try:
        converter = MarkdownCodeBlockConverter(args.directory)
        
        if args.dry_run:
            print("🔍 DRY RUN MODE - No files will be modified\n")
            # In dry run mode, we would show what would be changed
            markdown_files = converter.find_markdown_files()
            for file_path in markdown_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                code_blocks = converter.detect_indented_code_blocks(content)
                if code_blocks:
                    print(f"📝 {file_path.name}: Found {len(code_blocks)} indented code block(s)")
                else:
                    print(f"⏭️  {file_path.name}: No indented code blocks found")
        else:
            converter.process_all_files()
            
    except ValueError as e:
        print(f"❌ Error: {str(e)}")
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()