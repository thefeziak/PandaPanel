from flask import Flask
import configparser
import logging
import os
import sys
import threading
import time
from datetime import datetime

os.system('')

#sys.stdout = open(os.devnull, 'w')
#sys.stderr = open(os.devnull, 'w')

org_print = print

def log(what):
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    org_print(what)
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

print = log

config = configparser.ConfigParser()
config.read("panel.ini")
panel_name = config["panel"]["name"]
server_host = config["server"]["host"]
server_port = config["server"]["port"]
database_type = config["database"]["type"]
database_host = config["database"]["host"]
database_port = config["database"]["port"]
database_user = config["database"]["user"]
database_database = config["database"]["database"]
database_password = config["database"]["password"]

app = Flask(__name__)

from pages.index import bp as index_bp
app.register_blueprint(index_bp)

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
            
            if alladdr_ip == "":
                print("\033[38;5;250mPANDA\033[97mPANEL\033[0m > \033[1;92mRunning on:\033[0m")
            else:
                print(f"\033[38;5;250mPANDA\033[97mPANEL\033[0m > \033[1;92mRunning on all addresses ({alladdr_ip}):\033[0m")
            for ip in ips:
                print(f" - \033[38;5;196mhttp://{ip}\033[0m")
            print("\033[33mPress CTRL+C to quit\033[0m")
            return

if __name__ == "__main__":
    threading.Thread(target=app_informations).start()
    print(f" \033[48;5;15m\033[30mStarting Panel '{panel_name}'\033[0m")
    app.run(host=server_host, port=server_port)