# Python For Offensive PenTest: A Complete Practical Course - All rights reserved 
# Follow me on LinkedIn https://jo.linkedin.com/in/python2


# Basic TCP Client

import socket
import subprocess
from six.moves import input as raw_input

def connect(docker_proxy_port=18888):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(('0.0.0.0', docker_proxy_port))
    while True:
        command = raw_input("(edbpool)$ ")
        if b'terminate' or b'bye' in command:
            s.send(command)
            s.close()
            break 
        else:
            s.send(command)
            response = s.recv(2024)
            if response:
                print('{!r}'.format(response))
            else:
                pass

def main ():
    connect()

main()
