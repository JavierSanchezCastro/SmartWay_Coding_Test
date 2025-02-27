#!/bin/sh

#If the first argument is "generate_books", execute the script
if [ "$1" = "generate_books" ]; then
    python /backend/scripts/generate_books.py
    exit 0
fi

if [ "$1" = "statistics" ]; then
    python /backend/scripts/statistics.py
    exit 0
fi

#If not, execute the default backend
exec flask --app app --debug run -h 0.0.0.0 -p 80
