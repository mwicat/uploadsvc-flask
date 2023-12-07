#!/bin/sh

cd /app/src &&
exec python3 -m poetry run python -m flask --app=uploadsvc run --host=0.0.0.0 
