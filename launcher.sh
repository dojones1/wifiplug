#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /home/pi/workspaces
sudo python3 myHS100.py
cd /
