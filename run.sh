#!/bin/bash

source ./venv/bin/activate

# Update if needed
export DIALOG=/usr/bin/dialog

# Check if a language code argument is provided
if [ $# -eq 0 ]; then
    # Default to "en" if no argument is provided
    language_code="en"
else
    # Assign the first argument to a variable
    language_code=$1
fi

# Run the runner script with passed in language code
python3 ./src/runner.py "$language_code"