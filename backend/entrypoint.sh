#!/bin/sh

# Wait for database to be ready (in case we switch to PostgreSQL later)
sleep 2

# Create migrations
echo "Creating migrations..."
python manage.py makemigrations --noinput
python manage.py makemigrations api --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000