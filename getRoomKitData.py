import json
import os
import paramiko
import time
from pprint import pprint
import re
from dotenv import load_dotenv

load_dotenv()

def start_connect():
    """Connects to the host via ssh and outputs a channel object"""
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, int(port), username, password)
    return ssh

def send_command(ssh, command = "xstatus\r"):
    channel = ssh.invoke_shell()
    channel.send(command)
    while not channel.recv_ready():
        time.sleep(3)
    out = channel.recv(9999)
    string = out.decode('ascii')
    channel.close()
    return string


def data_to_dict(data, pattern='*s '):
    """converts the data you give it into a dictionary"""
    data = data.split(pattern)
    if pattern not in data[0]:
        data.pop(0)
    del data[-1]
    my_dict = {}
    for item in data:
        key, val = item.split(":", 1)
        my_dict[key] = val
    return my_dict


def dict_to_json(myDict, command, device):
    """spits out dict into a json file"""
    filename = f"/{device}_{command}_output.json"
    filepath = os.getenv("JSON_PATH")
    if os.path.exists(filepath) == False:
        os.mkdir(filepath)
    filename = f"{filepath}{filename}"
    with open(filepath, 'w') as fp:
        json.dump(myDict, fp)

def session_close(ssh):
    ssh.close()

def main():
    device = "swiney lab"
    command = "xstatus\r"
    session = start_connect()
    data = send_command(session, command)
    mydict = data_to_dict(data)
    dict_to_json(mydict, command, device)
    session_close()

if __name__ == "__main__":
    main()