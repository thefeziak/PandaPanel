from flask import Flask
import configparser
import logging
import os
import threading
import time
from datetime import datetime
from flask_login import LoginManager
from function_file import *
import sys

os.system('')

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

org_print = print
org_input = input

def log(what):
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    org_print(what)
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

print = log

def loginput(what):
    #sys.stdout = sys.__stdout__
    #sys.stderr = sys.__stderr__
    return_ = org_input(what)
    #sys.stdout = open(os.devnull, 'w')
    #sys.stderr = open(os.devnull, 'w')
    return return_

input = loginput

config = configparser.ConfigParser()
config.read("panel.ini")
panel_name = config["panel"]["name"]
panel_secret_key = config["panel"]["secret_key"]
server_host = config["server"]["host"]
server_port = config["server"]["port"]
smtp_host = config["smtp"]["host"]
smtp_port = config["smtp"]["port"]
smtp_user = config["smtp"]["user"]
smtp_password = config["smtp"]["password"]
smtp_from_address = config["smtp"]["from_address"]
smtp_from_name = config["smtp"]["from_name"]

app = Flask(__name__)
app.secret_key = panel_secret_key
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=3600)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=3600)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/auth/login'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

from pages.index import bp as index_bp
from pages.auth_login import bp as auth_login_bp
from pages.auth_logout import bp as auth_logout_bp
from pages.auth_password import bp as auth_password_bp
from pages.auth_password_reset import bp as auth_password_reset_bp
from pages.admin import bp as admin_bp
from pages.manage import bp as manage_bp
app.register_blueprint(index_bp)
app.register_blueprint(auth_login_bp)
app.register_blueprint(auth_logout_bp)
app.register_blueprint(auth_password_bp)
app.register_blueprint(auth_password_reset_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(manage_bp)

log_filename = "panel.log"
if os.path.exists(log_filename): os.remove(log_filename)

class logfilter1(logging.Filter):
    def filter(self, record):
        record.msg = record.msg.replace("[31m[1mWARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.[0m", "")
        return True
    
class logfilter2(logging.Filter):
    def filter(self, record):
        return "[33mPress CTRL+C to quit[0m" not in record.msg

class logfilter3(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        
        now = datetime.now()
        ftime = now.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        
        if not "Running on" in message:
            print(f"[{ftime}] - PANDAPANEL - {message}")
        
        return True

werkzeug = logging.getLogger("werkzeug")
werkzeug.setLevel(logging.DEBUG)

loghandler = logging.FileHandler(log_filename)
loghandler.addFilter(logfilter1())
loghandler.addFilter(logfilter2())
loghandler.addFilter(logfilter3())
formatter = logging.Formatter('[%(asctime)s] - PANDAPANEL - %(message)s')
loghandler.setFormatter(formatter)
werkzeug.addHandler(loghandler)

def app_informations():
    while True:
        if os.path.exists(log_filename):
            time.sleep(3)
            ips = []
            alladdr_ip = ""
            with open('panel.log', 'r') as logfile:
                for ip in logfile:
                    if ' * Running on' in ip:
                        ip = ip.strip()
                        if "all addresses" in ip:
                            ip = ip.replace('* Running on all addresses (', '').replace(')', '')
                            alladdr_ip = ip
                        if "http://" in ip:
                            ip = ip.replace('* Running on http://', '')
                            ips.append(ip)
            
            if len(ips) < 1:
                print(f"\033[38;5;250mPANDA\033[97mPANEL\033[0m > \033[1;92mCan`t run on http://{server_host}:{server_port}.\033[0m")
                sys.exit()
            if alladdr_ip == "":
                print("\033[38;5;250mPANDA\033[97mPANEL\033[0m > \033[1;92mRunning on:\033[0m")
            else:
                print(f"\033[38;5;250mPANDA\033[97mPANEL\033[0m > \033[1;92mRunning on all addresses ({alladdr_ip}):\033[0m")
            for ip in ips:
                print(f" - \033[38;5;196mhttp://{ip}\033[0m")
            print("\033[33mPress CTRL+C to quit\033[0m")
            return

if __name__ == "__main__":
    print(f" \033[48;5;15m\033[30mStarting Panel '{panel_name}'\033[0m")
    
    with open("file_data/file_data.json", "r") as file:
        users = json.load(file)["Users"]
    
    admin = "no"
    for user_id, user_data in users.items():
        if user_data.get("admin") == True:
            admin = "yes"
            break
    
    if admin == "no":
        print("\033[1;92mAdmin user not found! Create user:\033[0m")
        email = input("\033[33mEmail: \033[0m")

        username = input("\033[33mUsername: \033[0m")

        password = input("\033[33mPassword: \033[0m")

        password = hash_password(password)

        add_user(username, email, password, True)

    threading.Thread(target=app_informations).start()
    app.run(host=server_host, port=server_port)
