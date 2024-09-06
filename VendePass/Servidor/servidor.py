import socket
import threading
import networkx as nx
clients = []
origem = ''
destino = ''

def criar_grafo(arquivo):
    grafo = nx.Graph()
    with open(arquivo, 'r') as f:
        for linha in f:
            cidade1, cidade2 = linha.strip().split()
            grafo.add_edge(cidade1, cidade2)
    return grafo

grafo = criar_grafo('cidades.txt')

# Função para encontrar todos os caminhos entre duas cidades
def encontrar_caminhos(grafo, origem, destino):
    return list(nx.all_simple_paths(grafo, source=origem, target=destino))


#
def main():
    #abrindo socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #iniciando o servidor
    try:
        server.bind(('172.16.103.221', 777))
        server.listen(15)
    except:
        return print("Não foi possível iniciar o servidor")

    #servidor funcionando
    while True:
        client, addr = server.accept()
        clients.append(client)


        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()


#funções de envio de mensagem
def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            msg = list(msg)
            user = msg[0]
            origem = msg[1]
            destino = msg[2]
            msg = encontrar_caminhos(grafo, origem, destino)
            broadcast(msg, client)
        except:
            deleteClient(client)
            break

def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)

def deleteClient(client):
    clients.remove(client)


main()
