#!/bin/sh
# run aggregation script
python3 etl.py
# run trainig script
python3 training.py
# launch gunicorn
gunicorn -b :5000 --access-logfile - --error-logfile - application:app