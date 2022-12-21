#!/bin/sh

set -eux

# Run the app
gunicorn -c /code/src/project/config/wsgi_config.py run:app