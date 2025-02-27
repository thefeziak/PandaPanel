from flask import Blueprint, redirect, render_template
from flask_login import current_user
import configparser
from function_file import username_to_id, id_to_servers
import json

config = configparser.ConfigParser()
config.read("panel.ini")
panel_name = config["panel"]["name"]
if len(panel_name) > 12:
    to_remove = len(panel_name) - 12
    panel_name = panel_name[:-to_remove]

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect("/auth/login")
    user_id = username_to_id(current_user.get_id())
    file_data = json.load(open("file_data/file_data.json", "r"))
    admin = file_data["Users"][user_id]["admin"]
    servers = id_to_servers(user_id)
    return render_template("dash.html", name=panel_name, admin=admin, servers=servers)