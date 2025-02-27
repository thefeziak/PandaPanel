from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
import json
from datetime import datetime
import configparser
from function_file import *

config = configparser.ConfigParser()
config.read("panel.ini")
panel_name = config["panel"]["name"]
if len(panel_name) > 12:
    to_remove = len(panel_name) - 12
    panel_name = panel_name[:-to_remove]

bp = Blueprint('auth_password_reset', __name__)

@bp.route('/auth/password/reset', methods=['GET', 'POST'])
def auth_password_reset():
    if current_user.is_authenticated:
        return redirect("/")
    with open("file_data/file_data.json", "r") as file:
        file_data = json.load(file)
    
    users = file_data["Users"]
    forgot_password_keys = file_data["Forgot-Password-Keys"]
    
    reset_key = request.args.get("token", None)
    user_email = None

    for email, key_data in forgot_password_keys.items():
        if key_data["key"] == reset_key:
            user_email = email
            break

    if not user_email:
        return redirect("/auth/login")

    expiry_str = forgot_password_keys[user_email]["expiry"]
    expiry_time = datetime.fromisoformat(expiry_str)
    if datetime.now() > expiry_time:
        return redirect("/auth/login")

    if request.method == 'POST':
        new_password = request.form['password']

        user_id = None
        for uid, user_data in users.items():
            if user_data["email"] == user_email:
                user_id = uid
                break

        if not user_id:
            return render_template("password_reset.html", error="User not found.", name=panel_name)

        users[user_id]["password"] = hash_password(new_password)

        del forgot_password_keys[user_email]

        file_data["Users"] = users
        file_data["Forgot-Password-Keys"] = forgot_password_keys
        with open("file_data/file_data.json", "w") as file:
            json.dump(file_data, file, indent=4)

        return redirect("/auth/login")

    return render_template("password_reset.html", error="", name=panel_name)
