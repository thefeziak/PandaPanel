#!/bin/bash

apt update
apt install python3 python3-pip -y

cd /etc && mkdir Panda && cd Panda && mkdir Panel && cd Panel
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/server.py
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/function_file.py
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/requirements.txt
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/panel.ini
mkdir file_data && cd file_data && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/file_data/file_data.json && cd ..
mkdir templates && cd templates
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/admin.html
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/dash.html
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/login.html
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/manage.html
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/manage_console.html
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/password.html
wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/password_reset.html
cd ..
mkdir pages && cd pages
mkdir admin && cd admin && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/admin/__init__.py
mkdir auth_login && cd auth_login && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_login/__init__.py
mkdir auth_logout && cd auth_logout && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_logout/__init__.py
mkdir auth_password && cd auth_password && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_password/__init__.py
mkdir auth_password_reset && cd auth_password_reset && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_password_reset/__init__.py
mkdir index && cd index && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/index/__init__.py
mkdir manage && cd manage && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/manage/__init__.py
cd ..
mkdir static
mkdir css && cd css && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/css/style.css && cd ..
mkdir gif && cd gif && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/gif/background.gif && cd ..
mkdir js && cd js && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/js/mute.js && cd ..
mkdir png && cd png && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/png/logo.png && wget https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/png/server-icon.png && cd ..
cd ..
pip install -r requirements.txt
echo -e '#!/bin/bash\n\npython3 /etc/Panda/Node/server.py' | tee /bin/PandaNode > /dev/null && chmod +x /bin/PandaNode
echo "-----------------------------"
echo "Installed in /etc/Panda/Panel"
echo "Run using PandaPanel command!"
echo "-----------------------------"
