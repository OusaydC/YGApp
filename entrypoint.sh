#!/bin/sh
cd /app/WebAppYG
exec gunicorn yg_ma.wsgi:application --bind 0.0.0.0:${PORT:-8000}

