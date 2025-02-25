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
mkdir DockerConfiguration
cd DockerConfiguration
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/Dockerfile
docker build -t ubuntu2204 .
echo "---------- Done ----------"
echo " Installed in /Panda/Node "
echo "Run with python3 server.py"
echo "---------- Done ----------"
