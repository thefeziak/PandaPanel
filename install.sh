#!/bin/bash

OS_NAME=$(grep '^NAME=' /etc/os-release | cut -d'=' -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]')
OS_VERSION=$(grep '^VERSION_ID=' /etc/os-release | cut -d'=' -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]')

echo "######################################################################"
echo "* PandaPanel installation script @ v1.0.0"
echo "* https://github.com/thefeziak/PandaPanel"
echo "* Running $OS_NAME version $OS_VERSION."
echo "######################################################################"
echo "* What would you like to do?"
echo "* [0] Install Panel"
echo "* [1] Install Node"
echo "* [2] Install Both (Panel and Node)"
echo "* [3] Uninstall Panel or Node"
read -p "* Input 0-3: " OPTION

install_files() {
    local directory=$1
    local files=("${@:2}")
    for file in "${files[@]}"; do
        wget -q --show-progress -P "$directory" "$file"
    done
}

install_panel() {
    echo "* Installing Panel..."
    apt update
    apt install python3 python3-pip -y
    
    mkdir -p /etc/Panda/Panel/{file_data,templates,pages/{admin,auth_login,auth_logout,auth_password,auth_password_reset,index,manage},static/{css,gif,js,png}}

    cd /etc/Panda/Panel || exit
    
    install_files . \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/server.py" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/function_file.py" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/requirements.txt" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/panel.ini"

    install_files /etc/Panda/Panel/file_data \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/file_data/file_data.json"

    install_files /etc/Panda/Panel/templates \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/templates/admin.html" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/templates/dash.html" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/templates/login.html" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/templates/manage.html" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/templates/manage_console.html" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/templates/password.html" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/templates/password_reset.html"

    install_files /etc/Panda/Panel/pages/admin \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/admin/__init__.py"
    install_files /etc/Panda/Panel/pages/auth_login \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_login/__init__.py"
    install_files /etc/Panda/Panel/pages/auth_logout \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_logout/__init__.py"
    install_files /etc/Panda/Panel/pages/auth_password \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_password/__init__.py"
    install_files /etc/Panda/Panel/pages/auth_password_reset \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/auth_password_reset/__init__.py"
    install_files /etc/Panda/Panel/pages/index \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/index/__init__.py"
    install_files /etc/Panda/Panel/pages/manage \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/pages/manage/__init__.py"

    install_files /etc/Panda/Panel/static/css \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/css/style.css"
    install_files /etc/Panda/Panel/static/gif \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/gif/background.gif"
    install_files /etc/Panda/Panel/static/js \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/js/mute.js"
    install_files /etc/Panda/Panel/static/png \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/png/logo.png" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaPanel/static/png/server-icon.png"
    
    pip3 install -r /etc/Panda/Panel/requirements.txt
    
    echo -e '#!/bin/bash\n\ncd /etc/Panda/Panel/ && python3 server.py' | tee /usr/local/bin/PandaPanel > /dev/null
    chmod +x /usr/local/bin/PandaPanel
    
    echo "-----------------------------"
    echo "Installed in /etc/Panda/Panel"
    echo "Run using PandaPanel command!"
    echo "-----------------------------"
}

install_node() {
    echo "* Installing Node..."
    apt update
    apt install python3 python3-pip docker.io -y
    
    mkdir -p /etc/Panda/Node

    cd /etc/Panda/Node || exit
    install_files . \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/server.py" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/requirements.txt" \
        "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/config.json"

    pip install -r /etc/Panda/Node/requirements.txt
    
    mkdir DockerConfiguration
    cd DockerConfiguration
    wget -q --show-progress "https://raw.githubusercontent.com/thefeziak/PandaPanel/refs/heads/main/PandaNode/Dockerfile"
    docker build -t panduntu22-04 .
    
    echo -e '#!/bin/bash\n\nncd /etc/Panda/Node/ && python3 server.py' | tee /bin/PandaNode > /dev/null
    chmod +x /bin/PandaNode
    
    echo "---------- Done ------------"
    echo "Installed in /etc/Panda/Node"
    echo "Run using PandaNode command!"
    echo "---------- Done ------------"
}

uninstall() {
    local path=$1
    local name=$2
    if [ -d "$path" ]; then
        read -p "* $name detected. Would you like to uninstall? (y/n): " UNINSTALL
        if [ "$UNINSTALL" == "y" ]; then
            rm -rf "$path"
            echo "* $name uninstalled."
        else
            echo "* Operation canceled."
        fi
    fi
}

case "$OPTION" in
    0)
        install_panel
        ;;
    1)
        install_node
        ;;
    2)
        install_panel
        read -p "* Panel installed. Would you like to install Node? (y/n): " N_INSTALL
        if [ "$N_INSTALL" == "y" ]; then
            install_node
        else
            echo "* Operation canceled."
        fi
        ;;
    3)
        uninstall /etc/Panda/Panel "Panel"
        uninstall /etc/Panda/Node "Node"
        if [ ! -d "/etc/Panda/Panel" ] && [ ! -d "/etc/Panda/Node" ]; then
            echo "* Nothing to uninstall."
        fi
        ;;
    *)
        echo "* Invalid option."
        ;;
esac
