#!/bin/bash

# Initialize quotes if needed (simplified)
python3 -c "
import json
import os
quotes_file = os.getenv('QUOTES_FILE_PATH', '/app/quotes.json')
if not os.path.exists(quotes_file) or os.path.getsize(quotes_file) == 0:
    sample_quotes = [
        {'id': 1, 'text': 'The obstacle is the way.', 'author': 'Marcus Aurelius', 'source': 'Daily Stoic', 'date_added': '2025-01-01T00:00:00'},
        {'id': 2, 'text': 'You have power over your mind - not outside events. Realize this, and you will find strength.', 'author': 'Marcus Aurelius', 'source': 'Daily Stoic', 'date_added': '2025-01-01T00:00:00'},
        {'id': 3, 'text': 'It is not death that a man should fear, but he should fear never beginning to live.', 'author': 'Marcus Aurelius', 'source': 'Daily Stoic', 'date_added': '2025-01-01T00:00:00'}
    ]
    with open(quotes_file, 'w') as f:
        json.dump(sample_quotes, f, indent=2)
    print('Initialized quotes file')
else:
    print('Quotes file already exists')
"

# Start the application
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
