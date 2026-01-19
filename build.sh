#!/bin/bash
# Render build script - fixes setuptools for Python 3.13
set -e

# Upgrade pip, setuptools, wheel to latest versions (compatible with Python 3.13)
python -m pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r WebAppYG/requirements_minimal.txt

# Collect static files
cd WebAppYG
python manage.py collectstatic --noinput

