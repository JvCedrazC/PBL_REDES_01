import socket
import threading
import networkx as nx
import pickle

file = 'cidades.txt'
clients = []


def create_graph(arquivo):
    graph = nx.Graph()
    with open(arquivo, 'r') as f:
        for linha in f:
            cidade1, cidade2 = linha.strip().split()
            graph.add_edge(cidade1, cidade2)
    return graph


def find_path(source, target, graph):
    return list(nx.all_simple_paths(graph, source=source, target=target))


Graph0 = create_graph(file)


def send_path_to_client(client, msg):
    msg_loaded = pickle.loads(msg)
    source, target = msg_loaded[0], msg_loaded[1]
    print(source)
    print(target)
    path = find_path(source, target, Graph0)
    msg = pickle.dumps(path)
    client.sendall(msg)


def comunication(socket_client):
    while True:
        msg = socket_client.recv(1024)
        send_path_to_client(socket_client, msg)


def delete_client(client):
    clients.remove(client)


def main():

    #starting the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.246.54', 25565))
    server_socket.listen(15)

    while True:
        socket_client, addr = server_socket.accept()
        clients.append(socket_client)
        print(f'Cliente {socket_client.getsockname()[0]} conectado')

        thread = threading.Thread(target=comunication, args=[socket_client])
        thread.start()
        print('Aguardando conexão!')
        print('')


main()
