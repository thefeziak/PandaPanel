import subprocess
from flask import Flask, request, jsonify
import json

config = json.load(open("config.json", "r"))
secret_key_ = config["SECRET_KEY"]
host = config["HOST"]
port = config["PORT"]

app = Flask(__name__)

@app.route('/execute')
def execute():
    try:
        command = request.args.get('command')
        container_name = request.args.get('container')
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        cmd = f"docker exec -it {container_name} {command}"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 400
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/start')
def start():
    try:
        container_name = request.args.get('container')
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        cmd = f"docker start {container_name}"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 400
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/stop')
def stop():
    try:
        container_name = request.args.get('container')
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        cmd = f"docker stop {container_name}"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 400
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/restart', methods=['POST'])
def restart():
    try:
        container_name = request.args.get('container_name')
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        cmd = f"docker restart {container_name}"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 400
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/delete', methods=['POST'])
def delete():
    try:
        container_name = request.args.get('container')
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        cmd = f"docker rm {container_name}"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 400
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/create', methods=['POST'])
def create():
    try:
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        cmd = "docker run -itd --privileged --hostname panda --cap-add=ALL ubuntu:22.04"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 400
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host=host, port=port)
