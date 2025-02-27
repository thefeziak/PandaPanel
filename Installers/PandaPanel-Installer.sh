#!/bin/bash

apt update
apt install python3 python3-pip -y

mkdir -p /etc/Panda/Panel/file_data /etc/Panda/Panel/templates /etc/Panda/Panel/pages/admin /etc/Panda/Panel/pages/auth_login \
         /etc/Panda/Panel/pages/auth_logout /etc/Panda/Panel/pages/auth_password /etc/Panda/Panel/pages/auth_password_reset \
         /etc/Panda/Panel/pages/index /etc/Panda/Panel/pages/manage /etc/Panda/Panel/static/css /etc/Panda/Panel/static/gif \
         /etc/Panda/Panel/static/js /etc/Panda/Panel/static/png

cd /etc/Panda/Panel || exit

wget -q --show-progress https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/server.py
wget -q --show-progress https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/function_file.py
wget -q --show-progress https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/requirements.txt
wget -q --show-progress https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/panel.ini

wget -q --show-progress -P /etc/Panda/Panel/file_data https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/file_data/file_data.json

wget -q --show-progress -P /etc/Panda/Panel/templates https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/templates/{admin.html,dash.html,login.html,manage.html,manage_console.html,password.html,password_reset.html}

wget -q --show-progress -P /etc/Panda/Panel/pages/admin https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/admin/__init__.py
wget -q --show-progress -P /etc/Panda/Panel/pages/auth_login https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_login/__init__.py
wget -q --show-progress -P /etc/Panda/Panel/pages/auth_logout https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_logout/__init__.py
wget -q --show-progress -P /etc/Panda/Panel/pages/auth_password https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_password/__init__.py
wget -q --show-progress -P /etc/Panda/Panel/pages/auth_password_reset https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_password_reset/__init__.py
wget -q --show-progress -P /etc/Panda/Panel/pages/index https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/index/__init__.py
wget -q --show-progress -P /etc/Panda/Panel/pages/manage https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/manage/__init__.py

wget -q --show-progress -P /etc/Panda/Panel/static/css https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/css/style.css
wget -q --show-progress -P /etc/Panda/Panel/static/gif https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/gif/background.gif
wget -q --show-progress -P /etc/Panda/Panel/static/js https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/js/mute.js
wget -q --show-progress -P /etc/Panda/Panel/static/png https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/png/logo.png
wget -q --show-progress -P /etc/Panda/Panel/static/png https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/png/server-icon.png

pip3 install -r /etc/Panda/Panel/requirements.txt

echo -e '#!/bin/bash\n\npython3 /etc/Panda/Panel/server.py' | tee /usr/local/bin/PandaPanel > /dev/null
chmod +x /usr/local/bin/PandaPanel

echo "-----------------------------"
echo "Installed in /etc/Panda/Panel"
echo "Run using PandaPanel command!"
echo "-----------------------------"
