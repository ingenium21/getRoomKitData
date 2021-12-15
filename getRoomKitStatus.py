#! /usr/bin/python
from getRoomKitData import send_command, data_to_dict, dict_to_json, start_connect
from dotenv import load_dotenv
import os

load_dotenv()

def get_xstatus(session):
    command = "xStatus\r"
    commandTrimmed = "xStatus"
    data = send_command(session, command)
    # with open('./callHistory.txt', 'r') as ch:
    #     data = ch.read()    callsArray.pop(0)
    mydict = data_to_dict(data, pattern="*s ")
    dict_to_json(mydict, commandTrimmed)

def main():
    session = start_connect()
    get_xstatus(session)

if __name__ == "__main__":
    main()
