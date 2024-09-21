

import socket


client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_sock.connect(('192.168.246.7',25565))

msg = 'xana com xana é muito bacana'
while True:
    client_sock.send(input('Msg brother: ').encode())
    data = client_sock.recv(1024).decode()
    print(data)




client_sock.close()