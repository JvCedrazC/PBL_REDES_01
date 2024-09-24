import socket
import threading
import networkx as nx
import pickle

file = r"C:\Users\kmbma\OneDrive\Documentos\GitHub\PBL_REDES_01\Teste\TesteVendePass\Servidor\cidades.txt"
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
    try:
        msg_loaded = pickle.loads(msg)
        target, source, user = msg_loaded[2], msg_loaded[1], msg_loaded[0]
        print(f"Source: {source}, Target: {target}")

        # Verificar se os nós existem no grafo
        if source not in Graph0 or target not in Graph0:
            error_msg = f"Nó(s) não encontrado(s): {source} ou {target}."
            print(error_msg)
            client.sendall(pickle.dumps(error_msg))
            return
    
        path = find_path(source, target, Graph0)
    
        
        msg = pickle.dumps(path)
        client.sendall(msg)
    except pickle.UnpicklingError as e:
        print(f"Erro ao desempacotar a mensagem: {e}")
        client.sendall(pickle.dumps(f"Erro ao desempacotar a mensagem: {e}"))    
    except Exception as e:
        print(f"Erro ao encontrar caminho: {e}")
        client.sendall(pickle.dumps(f"Erro ao processar caminho: {e}"))


def comunication(socket_client):
    while True:
        msg = socket_client.recv(8192)
        send_path_to_client(socket_client, msg)


def delete_client(client):
    clients.remove(client)


def main():

    #starting the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.15.153', 5050))
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
