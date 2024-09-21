import socket
import threading

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


server.bind(('192.168.246.7',25565))
server.listen(3)



def sisirix(socket_client):
    print(f'Thread iniciada com cliente {socket_client.getsockname()}')
    while True:
        data = socket_client.recv(1024).decode()
        print(data)

        socket_client.send(input('cod: ').encode())
    socket_client.close()

while True:
    print('wrigwyugfhwajhuwr')
    socket_client, adr = server.accept()
    print(adr)
    threading.Thread(target=sisirix, args=[socket_client], daemon=True).start()