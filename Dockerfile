FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY WebAppYG/requirements_minimal.txt .

# Upgrade pip and install Python packages
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements_minimal.txt

# Copy application code
COPY . .

# Collect static files
WORKDIR /app/WebAppYG
RUN python manage.py collectstatic --noinput

# Copy and set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

# Run entrypoint
ENTRYPOINT ["/entrypoint.sh"]

