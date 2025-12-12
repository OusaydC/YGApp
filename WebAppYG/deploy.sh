#!/bin/bash
# Deployment script for DigitalOcean
# Run this script after initial server setup

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Activate virtual environment
source venv/bin/activate

# Pull latest code (if using git)
# git pull origin main

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Restart Gunicorn service
echo "🔄 Restarting Gunicorn..."
sudo systemctl restart yieldgap

echo "✅ Deployment complete!"
echo "Check status with: sudo systemctl status yieldgap"

