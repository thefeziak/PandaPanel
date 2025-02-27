from flask import Blueprint, render_template, request, redirect
import configparser
from flask_login import login_user, current_user
import json
from function_file import *

config = configparser.ConfigParser()
config.read("panel.ini")
panel_name = config["panel"]["name"]
if len(panel_name) > 12:
    to_remove = len(panel_name) - 12
    panel_name = panel_name[:-to_remove]

bp = Blueprint('auth_login', __name__)

@bp.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    if current_user.is_authenticated:
        return redirect("/")
    users = json.load(open("file_data/file_data.json", "r"))["Users"]
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']

        user_id = username_or_email_to_id(username_or_email)

        if user_id and unhash_password(users[user_id]['password'], password):
            user = User(users[user_id]['username'])
            login_user(user)
            return redirect("/")

        return render_template("login.html", name=panel_name, error="Invalid username/email or password!")
    
    return render_template("login.html", name=panel_name, error="")