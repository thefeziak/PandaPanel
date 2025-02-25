#!/bin/bash

apt update
apt install python3
apt install python3-pip
apt install docker.io

cd /
mkdir Panda
cd Panda
mkdir Node
cd Node
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/server.py
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/requirements.txt
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/config.json
pip install -r requirements.txt

echo "---------- Done ----------"
echo "Run with python3 server.py"
echo "---------- Done ----------"
