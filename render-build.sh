#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies and build frontend
cd frontend
npm install
REACT_APP_API_URL="" npm run build
cd ..

# Copy frontend build to backend static/templates
# Ensure directories exist
mkdir -p backend/static
mkdir -p backend/templates

# Copy files
cp -r frontend/build/static/* backend/static/
cp frontend/build/index.html backend/templates/
cp frontend/build/manifest.json backend/static/
cp frontend/build/*.png backend/static/
cp frontend/build/*.ico backend/static/

echo "Build successful!"
