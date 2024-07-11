#!/bin/bash
set -e

# Ensure that you have installed the necessary tools
pip install --upgrade setuptools wheel twine

# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build the source distribution and wheel
python setup.py sdist bdist_wheel

# Check the distribution files
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Add a condition to only upload on a specific branch, for example, 'main'
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" == "main" ]; then
    echo "Publishing to PyPI from the main branch."
    twine upload dist/*
else
    echo "Not on the main branch. Skipping PyPI upload."
fi
