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
    username = 'admin'
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


def data_to_dict(data="", pattern='*s ', filterPattern = ""):
    """converts the data you give it into a dictionary"""
    data = data.split(pattern)
    if pattern not in data[0]:
        data.pop(0)
    del data[-1]
    my_dict = {}
    for item in data:
        key, val = item.split(":", 1)
        if "(status=OK)" in key:
            continue #does some further trimming if you need it.
        key = re.sub(filterPattern, '', key)
        my_dict[key] = val.strip()
    return my_dict

def dict_to_json(myDict, command):
    """spits out dict into a json file"""
    device = os.getenv("DEVICE")
    command = command.replace(' ', '_')
    if command[-1] == "\r":
        del command[-1]
    filename = f"/{device}_{command}_output.json"
    filepath = os.getenv("JSON_PATH")
    if os.path.exists(filepath) == False:
        os.mkdir(filepath)
    filename = f"{filepath}{filename}"
    if os.path.exists(filename):
        with open(filename, 'rb+') as fp:
            fp.seek(-3, os.SEEK_END)
            fp.truncate()
        with open(filename, 'a', encoding='utf-8') as fp:
            fp.write(',\n')
            json.dump(myDict, fp)
            fp.write('\n]')
    else:
        with open(filename, 'a', encoding='utf-8') as fp:
            fp.write('[')
            json.dump(myDict, fp)
            fp.write('\n]')

def session_close(ssh):
    ssh.close()

def compare_callHistory_Ids(mydict):
    jsonFileName = "./local.json"
    if os.path.exists(jsonFileName):
        with open(jsonFileName, 'r') as j:
            callHistory = json.loads(j.read())
            j.close()
        if mydict[' CallId'] > callHistory[' CallId']:
            mydict = {' CallId' : mydict[' CallId']}
            with open(jsonFileName, 'w') as jn:
                json.dump(mydict, jn)
                jn.close()
            return True
        else:
            return False
    else:
        with open(jsonFileName, 'w') as jn:
                    json.dump(mydict, jn)
                    jn.close()
        return True

def get_call_history(session):
    command = "xcommand CallHistory Get DetailLevel: full\r"
    commandTrimmed = "callHistory"
    data = send_command(session, command)
    callsArray = re.split("\*r CallHistoryGetResult Entry \d CallHistoryId: \d+", data)
    callsArray.pop(0)
    for call in reversed(callsArray):
        mydict = data_to_dict(call, pattern="*r ", filterPattern="(.*?Entry \d)")
        cmp = compare_callHistory_Ids(mydict)
        if (cmp):
            dict_to_json(mydict, commandTrimmed)

def main():
    device = os.getenv("DEVICE")
    session = start_connect()
    get_call_history(session)


if __name__ == "__main__":
    main()