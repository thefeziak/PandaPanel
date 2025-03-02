from flask import Blueprint, redirect, render_template, request
from flask_login import current_user
import configparser
import requests
from function_file import username_to_id, list_servers, get_server_by_id, user_has_access, load_file_data
import json

config = configparser.ConfigParser()
config.read("panel.ini")
panel_name = config["panel"]["name"][:12]
secret_key = config["panel"]["secret_key"]

bp = Blueprint('manage', __name__)

def do_action(action, id, fd, cmd="None"):
    for node in fd["Nodes"].values():
        server = get_server_by_id(id, node["Servers"])
        if server:
            url = f"http://{node['Settings']['FQDN']}:{node['Settings']['Port']}/{action}?secret_key={secret_key}&container={id}&cmd={cmd}"
            try:
                result = requests.get(url).json()#, timeout=5).json()
                if "output" in result:
                    return result["output"]
                elif "error" in result:
                    return result["error"]
                return result
            except:
                return "Node is not responding."
    return "Node not found."

def manage_action(id, action, cmd="None"):
    if not current_user.is_authenticated:
        return redirect("/auth/login")
    
    user_id = username_to_id(current_user.get_id())
    file_data = load_file_data()
    server = get_server_by_id(id, list_servers())
    admin = user_has_access(user_id, server, file_data)
    
    if not server or not admin:
        return redirect("/")
    
    if action == "manage":
        return render_template("manage.html", name=panel_name, admin=admin)
    
    return do_action(action, id, file_data, cmd) if action else render_template("manage_console.html")

@bp.route('/manage/<id>')
def manage(id):
    return manage_action(id, "manage")

@bp.route('/manage/<id>/console')
def manage_console(id):
    return manage_action(id, None)

@bp.route('/manage/<id>/start')
def manage_start(id):
    return manage_action(id, "start")

@bp.route('/manage/<id>/stop')
def manage_stop(id):
    return manage_action(id, "stop")

@bp.route('/manage/<id>/restart')
def manage_restart(id):
    return manage_action(id, "restart")

@bp.route('/manage/<id>/delete')
def manage_delete(id):
    return manage_action(id, "delete")

@bp.route('/manage/<id>/console/execute')
def manage_execute(id):
    return manage_action(id, "execute", request.args["cmd"])
