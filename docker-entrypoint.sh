#!/bin/sh

set -eux

# Run the migrations
/usr/local/bin/flask db upgrade
# Run the app
gunicorn -c /code/src/project/config/wsgi_config.py run:app