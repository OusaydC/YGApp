#!/usr/bin/env bash
# Build script for Render
set -o errexit

# Upgrade pip and build tools first
python -m pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r WebAppYG/requirements.txt

# Collect static files
cd WebAppYG
python manage.py collectstatic --noinput

