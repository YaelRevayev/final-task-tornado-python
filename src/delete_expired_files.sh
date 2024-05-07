#!/bin/bash

# Use the directory path provided as the first argument
directory="$1"

# Run an infinite loop
while true; do
    find "$directory" -type f -cmin +1 -delete
    sleep 60
done

