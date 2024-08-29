import socket
import sys


def create_socket():
    global host
    global port
    global s

    host = ""
    port = 50007
    s = socket.socket()

