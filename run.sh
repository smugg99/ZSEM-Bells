#!/bin/bash

source ./venv/bin/activate

# Update if needed
export DIALOG=/usr/bin/dialog
export DIALOGRC=./dialogrc

# Assign the first argument to a variable
language_code=$1

source ./venv/bin/activate

# Run the runner script with passed in language code
python3 ./src/runner.py "$language_code"