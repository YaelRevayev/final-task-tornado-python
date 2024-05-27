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
sudo xargs -a packages.txt apt-get install -y

# Enable and start pure-ftpd service
sudo systemctl enable pure-ftpd
sudo systemctl start pure-ftpd

# Enable and start redis-server service
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Download and install Filebeat
sudo wget -P /home/ https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.16.3-amd64.deb
sudo dpkg -i /home/filebeat-7.16.3-amd64.deb

# Enable and start filebeat service
sudo systemctl enable filebeat
sudo systemctl start filebeat

echo "All packages have been installed."
