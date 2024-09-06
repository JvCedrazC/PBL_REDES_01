import socket
import threading
import PBL_REDES_01.VendePass.Cliente

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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipv4 = str(get_ipv4())

    try:
        client.connect((ipv4, 777))
    except:
        return print("\n Não foi possível conectar ao servidor")

    print("Conectado!\n")

    user = input("Nome do usuário>")
    origem = 'B'
    destino = 'E'

    thread1 = threading.Thread(target=receive_Messages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, user, origem, destino])

    thread1.start()
    thread2.start()


#receber mensagens
def receive_Messages(client):
    while True:
        try:
            msg = client.recv(2048)#.decode('utf-8')
            for i in msg:
                print(i + '\n')
        except:
            print('\nNão foi possível permancer conectado ao servidor!')
            print('\nPressione <enter> para continuar')
            client.close()
            break

#enviar mensagens
def sendMessages(client, user, origem, destino):
    while True:
        try:
            client.send(user.encode('utf-8'), origem.encode('utf-8'), destino.encode('utf-8'))
        except:
            return



