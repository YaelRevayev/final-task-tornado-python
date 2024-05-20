#!/bin/bash

directory="$1"

while true; do
    find "$directory" -type f -cmin +1 -delete
    sleep 60
done

