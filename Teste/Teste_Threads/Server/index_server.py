import threading
import socket
clients = []

def get_ipv4():
    # Tenta criar uma conexão para obter o IP da máquina local
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Conecta a um IP externo para obter o IP local (não será enviado nenhum dado)
        s.connect(("8.8.8.8", 80))  # Usa o DNS do Google como referência
        ipv4 = s.getsockname()[0]
    except Exception as e:
        ipv4 = "Não foi possível obter o IPv4"
    finally:
        s.close()
    return ipv4

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipv4 = str(get_ipv4())
    try:
        server.bind((ipv4, 777))
        server.listen(15)
    except:
        return print("Não foi possível iniciar o servidor")
    while True:
        client, addr = server.accept()
        clients.append(client)

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            sendClients(msg, client)
        except:
            deleteClient(client)
            break

def sendClients(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)

def deleteClient(client):
    clients.remove(client)

main()