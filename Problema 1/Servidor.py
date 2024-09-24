import random
import socket
import pickle
import threading
import networkx as nx

list_clients = []
clients_lock = threading.Lock()

file = 'cidades.txt'


def create_graph(file):
    graph = nx.Graph()
    with open(file, 'r') as f:
        for linha in f:
            cidade1, cidade2 = linha.strip().split()
            graph.add_edge(cidade1, cidade2)
    return graph


def find_path(graph, source, target):
    return list(nx.all_simple_paths(graph, source=source, target=target))


graph = create_graph(file)


def generate_tickets(all_paths):
    rotes_tickets = {}
    for path in all_paths:
        tickets = random.randint(0, 6)
        place = ' -> '.join(path)
        rotes_tickets[place] = tickets
    return rotes_tickets


# Armazena as rotas disponíveis globalmente
rotes_tickets = {}


def print_rotas(rotas, mensagem):
    print(mensagem)
    for rota, passagens in rotas.items():
        print(f"Rota: {rota}, Passagens disponíveis: {passagens}")
    print("\n")


def communication(socket_client):
    global rotes_tickets
    try:
        while True:
            msg = socket_client.recv(8192)
            if not msg:
                break  # Se não houver mensagem, o cliente se desconectou

            data = pickle.loads(msg)
            # Verifica o tipo de dado recebido: lista de pedido ou dicionário atualizado
            if isinstance(data, list):
                source, target, type_of_request = data[0], data[1], data[2]
                print(f'Source: {source}, Target: {target}, Type of request: {type_of_request}')

                if type_of_request == 0:
                    with clients_lock:
                        if socket_client in list_clients:
                            print('Calculando rotas...')
                            all_paths = find_path(graph, source, target)
                            all_paths = [path for path in all_paths if len(path) <= 4]  # Filtra rotas com mais de 4 cidades
                            print('Rotas calculadas:', all_paths)

                            # Limita as rotas a no máximo 3 antes de gerar os tickets
                            all_paths = all_paths[:3]

                            rotes_tickets = generate_tickets(all_paths)

                            # Print rotas antes de enviar ao cliente
                            print_rotas(rotes_tickets, "Rotas e vagas antes de enviar para o cliente:")

                            msg_to_client = pickle.dumps(rotes_tickets)
                            print('Enviando Rotas...')
                            socket_client.sendall(msg_to_client)
                            print('Rotas enviadas!')
                        else:
                            print('Cliente desconectado')

            elif isinstance(data, dict):
                # Recebe o dicionário atualizado de volta do cliente
                with clients_lock:
                    print('Atualização de passagens recebida do cliente.')
                    print_rotas(data, "Rotas e vagas recebidas do cliente:")

                    rotes_tickets.update(data)  # Atualiza as rotas com os novos valores de passagens


    except Exception as e:
        print(f'Erro na comunicação: {e}')
    finally:
        with clients_lock:
            if socket_client in list_clients:
                list_clients.remove(socket_client)  # Remove cliente desconectado
        socket_client.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 777))
    server.listen(15)
    print("Servidor escutando na porta 777...")

    while True:
        try:
            socket_client, addr = server.accept()
            with clients_lock:
                list_clients.append(socket_client)
            print(f'Cliente conectado: {addr}')
            thread = threading.Thread(target=communication, args=[socket_client])
            thread.start()
            print("Thread Iniciada...")
        except Exception as e:
            print(f'Erro ao aceitar conexão: {e}')


if __name__ == "__main__":
    main()
