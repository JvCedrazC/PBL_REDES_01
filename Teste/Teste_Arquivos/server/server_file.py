import threading
import socket
clients = []

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipv4 = 'localhost'
    try:
        server.bind((ipv4, 777))
        server.listen(15)
    except:
        return print("Não foi possível iniciar o servidor")
    while True:
        client, addr = server.accept()
        namefile = client.recv(2048).decode()

        with open(namefile, 'rb') as file:
            for data in file.readlines():
                client.send(data)

            print('Arquivo enviado!')
main()


