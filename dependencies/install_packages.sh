#!/bin/bash
set -e
# Update the package list
sudo apt-get update
# Install prerequisites for adding new repositories
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Install packages listed in packages.txt
sudo xargs -a packages.txt apt-get install -y
sudo systemctl enable pure-ftpd
sudo systemctl start pure-ftpd
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo su
# Download and install Filebeat
wget -P /home/ https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.16.3-amd64.deb
cd /home/
dpkg -i filebeat-7.16.3-amd64.deb
echo "All packages have been installed."
