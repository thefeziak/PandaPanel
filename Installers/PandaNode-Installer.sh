#!/bin/bash

apt update
apt install python3 python3-pip docker.io -y

cd /etc && mkdir Panda && cd Panda && mkdir Node && cd Node
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/server.py
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/requirements.txt
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/config.json
pip install -r /etc/Panda/Node/requirements.txt
mkdir DockerConfiguration
cd DockerConfiguration
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/Dockerfile
docker build -t ubuntu2204 .
echo -e '#!/bin/bash\n\npython3 /etc/Panda/Node/server.py' | tee /bin/PandaNode > /dev/null && chmod +x /bin/PandaNode
echo "---------- Done ------------"
echo "Installed in /etc/Panda/Node"
echo "Run using PandaNode command!"
echo "---------- Done ------------"
