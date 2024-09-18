import socket
import threading
import networkx as nx
import pickle

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
    #abrindo socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipv4 = str(get_ipv4())
   # ipv4 = '192.168.7.54'

    #iniciando o servidor
    try:
        server.bind((ipv4, 8080))
        server.listen(15)

    except:
        return print("Servidor não iniciado!")
    print('Servidor abriu')
    print(f'IP: {ipv4}')
    #servidor funcionando
    while True:
        client, addr = server.accept()
        clients.append(client)
        print('cliente conectado!')
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()
        res = input('>')
        if res == 's':
            print(clients)
            '''if len(clients) != 0:
                for i in clients:
                    print(f'{i}\n')
            else:
                print("Não há clientes conectados!")'''



#funções de envio de mensagem
def messagesTreatment(client):
    while True:
        try:
            msg = eval(client.recv(4096))
            lista = pickle.loads(msg)
            print('Mensagem recebida')
            origem = msg[2]
            print(f'Origem: {origem}')
            destino = msg[3]
            print(f'Destino: {destino}')
            caminhos = encontrar_caminhos(grafo, origem, destino)
            for i in caminhos:
                print(f'Caminho: {i}')
            send_paths = pickle.dumps(caminhos)
            broadcast(send_paths, client)

        except:
            deleteClient(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem == client:
            try:
                clientItem.send(msg)
            except:
                print('Cliente não conectado!')
    print('Mensagem enviada')
def deleteClient(client):
    clients.remove(client)


main()
