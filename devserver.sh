#!/bin/sh
set -e

# Activate Python virtual environment
echo "--- Activating Python virtual environment..."
source .venv/bin/activate

# Install node dependencies
echo "--- Installing/verifying npm dependencies..."
npm install --silent

# Clean up old css file
echo "--- Removing old tailwind.css if it exists..."
rm -f ./static/css/tailwind.css

# Run the initial CSS build
echo "--- Running initial Tailwind CSS build..."
npm run build:css

# Verify that the CSS file was created
echo "--- Verifying CSS file creation..."
ls -l ./static/css/

# Start the CSS watch process in the background
echo "--- Starting Tailwind CSS watch process in background..."
npm run watch:css &

# Start the Flask server
echo "--- Starting Flask server..."
flask --app main run --host=0.0.0.0 --port=$PORT --debug

# Kill the background watch process when the server stops
kill %1
