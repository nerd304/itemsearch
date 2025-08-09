#!/usr/bin/env bash

# Exit on error
set -o errexit

# Run the production server
gunicorn main:app -b 0.0.0.0:$PORT
