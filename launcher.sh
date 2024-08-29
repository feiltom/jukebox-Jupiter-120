#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
sleep 5
cd /
cd home/jukebox/
date >>/home/jukebox/logs/cronlog
export XDG_RUNTIME_DIR=/run/user/1000
sudo python jukebox.py >>/home/jukebox/logs/cronlog 2>&1
cd /