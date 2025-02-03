from flask import Blueprint, render_template
import configparser

config = configparser.ConfigParser()
config.read("panel.ini")
panel_name = config["panel"]["name"]
if len(panel_name) > 12:
    to_remove = len(panel_name) - 12
    panel_name = panel_name[:-to_remove]

bp = Blueprint('auth_login', __name__)

@bp.route('/auth/login')
def auth_login():
    return render_template("login.html", name=panel_name)