#!/bin/bash
# Render build script

set -e

echo "=== Render Build Script ==="

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully"