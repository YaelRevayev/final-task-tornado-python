#!/bin/bash
set -e

# Update the package list
sudo apt-get update

# Install prerequisites for adding new repositories
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Ensure necessary directories exist
mkdir -p logs
mkdir -p files_output

# Install packages listed in packages.txt
if [ -f packages.txt ]; then
    while IFS= read -r package; do
        sudo apt-get install -y "$package"
    done < packages.txt
else
    echo "packages.txt not found."
    exit 1
fi

# Enable and start pure-ftpd and redis-server services
sudo systemctl enable pure-ftpd
sudo systemctl start pure-ftpd
sudo systemctl enable redis-server
sudo systemctl start redis-server


echo "All packages have been installed."
