#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install Pillow separately with specific flags
pip install --no-cache-dir --force-reinstall Pillow==10.0.1

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate 