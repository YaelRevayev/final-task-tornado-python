#!/bin/bash

directory="/home/pure-ftpd-server/final-task-tornado-python/files_output"

# Run an infinite loop
while true; do
    find "$directory" -type f -cmin +1 -delete
    sleep 60
done
