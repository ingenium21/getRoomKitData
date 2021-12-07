import json
import os
import paramiko
import time
from pprint import pprint
import re
from dotenv import load_dotenv

load_dotenv()

def start_connect():
    """Connects to the host via ssh"""
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, int(port), username, password)
    channel = ssh.invoke_shell()
    channel.send("xstatus\r")
    while not channel.recv_ready():
        time.sleep(3)
    out = channel.recv(9999)
    string = out.decode('ascii')
    channel.close()
    ssh.close()
    return string


def data_to_dict(data):
    """converts the data you give it into a dictionary"""
    data = data.split('*s ')
    data.pop(0)
    del data[-1]
    my_dict = {}
    for item in data:
        key, val = item.split(":", 1)
        my_dict[key] = val
    return my_dict


def dict_to_json(myDict):
    """spits out dict into a json file"""
    filepath = os.getenv("JSON_PATH")
    with open(filepath, 'w') as fp:
        json.dump(myDict, fp)

def main():
    data = start_connect()
    mydict = data_to_dict(data)
    dict_to_json(mydict)


if __name__ == "__main__":
    main()