# !/bin/bash

# Build the project
echo "Building the project..."
python3.11 -m pip3 install -r requirements.txt

echo "Make migration..."
python3.11 manage.py makemigrations --noinput
python3.11 manage.py migrate --noinput

echo "Collect static"
python3.11 manage.py collectstatic --noinput --clear