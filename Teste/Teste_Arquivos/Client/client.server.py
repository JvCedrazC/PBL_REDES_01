import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 777))
    except:
        return print("\n Não foi possível conectar ao servidor")
    print("Conectado!")
    name_file = input("Arquivo>")
    client.send(name_file.encode())

    with open(name_file, 'wb') as file:
        while 1:
            data = client.recv(10000)
            if not data:
                break
            file.write(data)
    print(f'{name_file} recebido!\n')
main()