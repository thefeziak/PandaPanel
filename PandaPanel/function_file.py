from flask_login import UserMixin
import json
import uuid
from datetime import datetime, timedelta
import hashlib

def hash_password(password: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    
    return sha256.hexdigest()

def unhash_password(stored_hash: str, input_password: str) -> bool:
    return stored_hash == hash_password(input_password)

class User(UserMixin):
    def __init__(self, username):
        self.id = username

def generate_password_reset(email):
    with open("file_data/file_data.json", "r") as file:
        filedata = json.load(file)

    fpk = filedata["Forgot-Password-Keys"]
    
    if email in fpk:
        existing_entry = fpk[email]
        expiry_time = datetime.fromisoformat(existing_entry["expiry"])
        
        if datetime.now() < expiry_time:
            return existing_entry["key"]
    
    new_key = str(uuid.uuid4())
    expiry_time = datetime.now() + timedelta(hours=3)

    fpk[email] = {
        "key": new_key,
        "expiry": expiry_time.isoformat()
    }
    filedata["Forgot-Password-Keys"] = fpk

    with open("file_data/file_data.json", "w") as file:
        json.dump(filedata, file, indent=4)

    return new_key

def generate_user_id(userdata):
    id = str(uuid.uuid4()).replace("-", "")[:-8]
    if id not in userdata:
        return id
    else:
        return generate_user_id(userdata)

def add_user(username, email, password, admin):
    with open("file_data/file_data.json", "r") as file:
        filedata = json.load(file)
    id = generate_user_id(filedata["Users"])
    filedata["Users"][id] = {
        "username": username,
        "email": email,
        "password": password,
        "admin": admin
    }
    with open("file_data/file_data.json", "w") as filew:
        json.dump(filedata, filew, indent=4)

def remove_user(id):
    with open("file_data/file_data.json", "r") as file:
        filedata = json.load(file)
    del filedata["Users"][id]
    with open("file_data/file_data.json", "w") as filew:
        json.dump(filedata, filew, indent=4)

def email_to_id(email):
    users = json.load(open("file_data/file_data.json", "r"))["Users"]
    id = next((user_id for user_id, user_data in users.items() if user_data['email'] == email), None)
    return id

def username_to_id(username):
    users = json.load(open("file_data/file_data.json", "r"))["Users"]
    id = next((user_id for user_id, user_data in users.items() if user_data['username'] == username), None)
    return id

def username_or_email_to_id(username_or_email):
    users = json.load(open("file_data/file_data.json", "r"))["Users"]
    id = next((user_id for user_id, user_data in users.items() 
                        if user_data['username'] == username_or_email or user_data['email'] == username_or_email), None)
    return id

def id_to_servers(id):
    nodes = json.load(open("file_data/file_data.json", "r"))["Nodes"]
    servers = []
    for node_name, node_data in nodes.items():
        for server in node_data["Servers"]:
            if server["owner"] == id:
                servers.append(server)
    return servers

def list_servers():
    nodes = json.load(open("file_data/file_data.json", "r"))["Nodes"]
    servers = []
    for node_name, node_data in nodes.items():
        for server in node_data["Servers"]:
            servers.append(server)
    return servers

def get_server_by_id(id, servers):
    return next((s for s in servers if s["id"] == id), None)

def load_file_data():
    with open("file_data/file_data.json", "r") as f:
        return json.load(f)

def user_has_access(user_id, server, file_data):
    return file_data["Users"].get(user_id, {}).get("admin", False) or user_id == server["owner"]