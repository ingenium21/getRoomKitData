import json
import os
import paramiko
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

    session = ssh.connect(os.getenvHOST,PORT,USERNAME,PASSWORD)
    return session

def run_command(session, command = "xstatus"):
    """runs the command in the ssh session"""
    (stdin, stdout, stderr) = session.exec_command(remote_cmd)
    pprint(stdout)
    if stderr:
        return stderr
    elif stdout:
        return stdout
    else:
        print("failed to produce either an stdout or an stderr")
        return stdin

def data_to_dict(data=""):
    """converts the data you give it into a dictionary"""
    my_dict = {}
    file = open("./stdout.txt", 'r')
    data1 = file.readlines()
    for item in data1:
        item = item[3:]
        item = item.strip()
        key, val = item.split(":", 1)
        my_dict[key] = val
    return my_dict


def dict_to_json(myDict):
    """spits out dict into a json file"""
    filepath = os.getenv("JSON_PATH")
    with open(filepath, 'w') as fp:
        json.dump(myDict, fp)

def main():
    data = data_to_dict()
    dict_to_json(data)


if __name__ == "__main__":
    main()