# Makefile for Markdown Code Block Converter

.PHONY: help test run-dry run clean install

# Default target
help:
	@echo "Available commands:"
	@echo "  make test      - Run unit tests"
	@echo "  make run-dry   - Run converter in dry-run mode on current directory" 
	@echo "  make run       - Run converter on current directory"
	@echo "  make clean     - Clean up temporary files"
	@echo "  make install   - Set up virtual environment (already done)"

# Run unit tests
test:
	python -m unittest test_converter.py -v

# Run in dry-run mode
run-dry:
	python md_codeblock_converter.py --dry-run

# Run the converter
run:
	python md_codeblock_converter.py

# Clean temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name ".DS_Store" -delete

# Note: Virtual environment is already set up
install:
	@echo "Virtual environment already configured at:"
	@echo ".venv/bin/python"
	@echo ""
	@echo "To activate manually:"
	@echo "source .venv/bin/activate"