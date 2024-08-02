#!/bin/bash

PROGRAM_NAME="HVACchatGPT.py"

# Check if the program is already running
if pgrep -x "$PROGRAM_NAME" > /dev/null
then
    echo "Program is already running."
    exit 1
fi

# Start the program
./$PROGRAM_NAME &