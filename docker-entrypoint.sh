#!/bin/sh

set -eux
if [ "x$RUN_UPGRADE" = 'x1' ]; then

    # Add any commands that depend on the database here (such as database migrations)
    /usr/local/bin/flask db upgrade

    echo "Migration should have run."
    
fi

exec "$@"

# Run the app
gunicorn -c /code/src/project/config/wsgi_config.py run:app