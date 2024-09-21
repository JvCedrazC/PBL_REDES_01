import socket
import pickle

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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipv4 = str(get_ipv4())
client.connect((ipv4, 777))
lista = ['User', 'Origem', 'Destino']
lista = pickle.dumps(lista)
client.sendall(lista)