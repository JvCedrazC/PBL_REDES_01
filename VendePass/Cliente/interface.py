import socket
import threading
import PBL_REDES_01.VendePass.Cliente

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('172.16.103.221', 777))
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



