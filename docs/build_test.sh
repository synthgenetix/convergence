#!/bin/bash
# Test documentation build

echo "Testing Sphinx documentation build..."

# Clean previous builds
rm -rf _build

# Build HTML docs
sphinx-build -b html . _build/html -W --keep-going

echo "Build complete. Check _build/html/index.html"