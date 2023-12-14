#!/bin/sh

exec poetry run gunicorn \
    --bind '0.0.0.0:5000' \
    --chdir src \
    'uploadsvc:app'
