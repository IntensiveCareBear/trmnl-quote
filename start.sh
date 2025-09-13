#!/bin/bash

# Initialize quotes if needed
python3 -c "
import sys
sys.path.append('/app')
from app import initialize_quotes
initialize_quotes()
"

# Start the application
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
