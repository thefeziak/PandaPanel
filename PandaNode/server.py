import subprocess
from flask import Flask, request, jsonify
import json
import asyncio

config = json.load(open("config.json", "r"))
secret_key_ = config["SECRET_KEY"]
host = config["HOST"]
port = config["PORT"]

app = Flask(__name__)

async def capture_tmate_session_line(process):
    while True:
        output = await process.stdout.readline()
        if not output:
            break
        output = output.decode('utf-8').strip()
        if "ssh session:" in output:
            return output.split("ssh session:")[1].strip()
    return None

async def capture_sshx_session_line(process):
    while True:
        output = await process.stdout.readline()
        if not output:
            break
        output = output.decode('utf-8').strip()
        if "Link:" in output:
            return output.split("ssh session:")[1].strip()
    return None

@app.route('/execute')
def execute():
    try:
        command = request.args.get('cmd')
        container_name = request.args.get('container')
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        cmd = f'docker exec {container_name} bash -c "{command}"'

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'output': result.stderr}), 400
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'output': str(e)}), 400

@app.route('/tmate')
async def tmate():
    try:
        command = request.args.get('cmd')
        container_name = request.args.get('container')
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        try:
            exec_cmd = await asyncio.create_subprocess_exec("docker", "exec", container_name, "tmate", "-F", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            return jsonify({'output': str(e)}), 400

        ssh_session_line = await capture_tmate_session_line(exec_cmd)

        return jsonify({'output': ssh_session_line})
    except Exception as e:
        return jsonify({'output': str(e)}), 400

@app.route('/sshx')
async def sshx():
    try:
        command = request.args.get('cmd')
        container_name = request.args.get('container')
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        try:
            exec_cmd = await asyncio.create_subprocess_exec("docker", "exec", container_name, "sshx", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            return jsonify({'output': str(e)}), 400

        ssh_session_line = await capture_sshx_session_line(exec_cmd)

        return jsonify({'output': ssh_session_line})
    except Exception as e:
        return jsonify({'output': str(e)}), 400
    
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
    
@app.route('/restart')
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
    
@app.route('/delete')
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
    
@app.route('/create')
def create():
    try:
        secret_key = request.args.get('secret_key')

        if secret_key != secret_key_:
            return jsonify({'error': "Invalid secret key."}), 400

        cmd = "docker run -itd --privileged --hostname panda --cap-add=ALL ubuntu2204"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 400
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host=host, port=port)
