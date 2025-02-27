from flask import Blueprint, render_template, request, redirect
from flask_login import current_user
import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from function_file import *

config = configparser.ConfigParser()
config.read("panel.ini")
panel_name = config["panel"]["name"]
if len(panel_name) > 12:
    to_remove = len(panel_name) - 12
    panel_name = panel_name[:-to_remove]

smtp_host = config["smtp"]["host"]
smtp_port = int(config["smtp"]["port"])
smtp_user = config["smtp"]["user"]
smtp_password = config["smtp"]["password"]
smtp_from_address = config["smtp"]["from_address"]
smtp_from_name = config["smtp"]["from_name"]

bp = Blueprint('auth_password', __name__)

@bp.route('/auth/password', methods=['GET', 'POST'])
def auth_password():
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        email = request.form['email']

        user_id = email_to_id(email)

        if user_id:
            id = generate_password_reset(email)
            reset_link = f"http://127.0.0.1/auth/password/reset?token={id}"
            send_reset_email(email, reset_link)
            return render_template("password.html", name=panel_name, error="The email has been sent.")

        return render_template("password.html", name=panel_name, error="Email not found!")

    return render_template("password.html", name=panel_name, error="")

def send_reset_email(email, reset_link):
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center; margin: 0; padding: 20px; background-color: #f9f9f9;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #333;">Password Reset Request</h2>
                <p style="color: #555;">Click the button below to reset your password:</p>
                <a href="{reset_link}" 
                   style="display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; 
                          text-decoration: none; font-size: 16px; border-radius: 5px; margin: 20px 0;">
                   Reset Your Password
                </a>
                <p style="color: #777;">If you did not request this, you can safely ignore this email.</p>
                <p style="color: #777;">If button don`t work just copy this link: {reset_link} and paste in to browser.</p>
            </div>
            <footer style="margin-top: 20px; font-size: 14px; color: #888;">
                © 2025 PandaPanel All rights reserved.
            </footer>
        </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Password Reset"
    msg['From'] = f"{smtp_from_name} <{smtp_from_address}>"
    msg['To'] = email

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_from_address, [email], msg.as_string())
    except Exception as e:
        print(str(e))