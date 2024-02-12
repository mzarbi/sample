#!/bin/bash

# Start Gunicorn with the number of workers specified by the GUNICORN_WORKERS environment variable
gunicorn -w ${GUNICORN_WORKERS:-4} -b 0.0.0.0:5000 run:app