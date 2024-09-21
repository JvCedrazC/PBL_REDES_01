import pickle
import networkx as nx
import socket
import threading

def cidades(numero):
    if numero == 1:
        return "Sao_Paulo"
    elif numero == 2:
        return "Rio_de_Janeiro"
    elif numero == 3:
        return "Brasilia"
    elif numero == 4:
        return "Salvador"
    elif numero == 5:
        return "Recife"
    elif numero == 6:
        return "Porto_Alegre"
    elif numero == 7:
        return "Curitiba"
    elif numero == 8:
        return "Fortaleza"
    elif numero == 9:
        return "Manaus"
    elif numero == 10:
        return "Belo_Horizonte"
        
        


def validarEntradas(numero):
    if numero < 1 or numero > 10:
        while True:
            numero = int(input("Escolha um local válido:\n 1 = São Paulo (SP)\n 2 = Rio de Janeiro (RS)\n 3 = Brasília (DF) \n 4 = Salvador (BA)\n 5 = Recife (PE)\n 6 = Porto Alegre (RS)F\n 7 = Curitiba (PR)\n 8 = Fortaleza (CE)\n 9 = Manaus (AM)\n 10 = Belo Horizonte (BH)\n 11 = Para sair"))
            if numero >= 1 or numero <= 11:
                return
    else:
        return
    
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

#receber mensagens
def receive_Messages(client):
    while True:
        try:
            msg = client.recv(4096)#.decode('utf-8')
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
            #client.send(user.encode('utf-8'), origem.encode('utf-8'), destino.encode('utf-8'))
            data = pickle.dumps([user, origem, destino])
            client.send(data)
        except Exception as e:
            print((f"Erro ao enviar: {e}"))
            return


def main():
    sair = 0

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Cliente socket entrou")
    ipv4 = str(get_ipv4())

    try:
        client.connect(('192.168.15.153', 5050))
        print("Tentou entrar aqui!")

    except:
        return print("\n Não foi possível conectar ao servidor")

    print("Conectado!\n")


    while sair == 0:
        print("\n")
        print(100*"=")
        print("-------- Bem vindo a foda-se --------")
        print("\n")
        
        nome = input("Digite o seu nome: ")
        print(100*"=")


        print("Escolha o número que represente o seu local de origem (local de onde você quer viajar):\n 1 = São Paulo (SP)\n 2 = Rio de Janeiro (RS)\n 3 = Brasília (DF) \n 4 = Salvador (BA)\n 5 = Recife (PE)\n 6 = Porto Alegre (RS)F\n 7 = Curitiba (PR)\n 8 = Fortaleza (CE)\n 9 = Manaus (AM)\n 10 = Belo Horizonte (BH)\n 11 = Para sair")
        origem = int(input("Origem: "))
        
        #Tratamento de erro / Desistência do usuario
        if origem == 11:
            break

        #Validar entrada de origem        
        validar = validarEntradas(origem)
        origem = cidades(origem)
        
        print("\n")
        print(100*"=")
        print("\nAgora escolha o número que represente o seu local de destino (local para onde você quer viajar):\n 1 = São Paulo (SP)\n 2 = Rio de Janeiro (RS)\n 3 = Brasília (DF) \n 4 = Salvador (BA)\n 5 = Recife (PE)\n 6 =Porto Alegre (RS)F\n 7 = Curitiba (PR)\n 8 = Fortaleza (CE)\n 9 = Manaus (AM)\n 10 = Belo Horizonte (BH)\n 11 = Para sair")
        destino = int(input("Destino: "))
        if destino == 11:
            break
        
        #Validar entrada de destino
        validar = validarEntradas(destino)
        destino = cidades(destino)
        print("Enviando")


        
        thread1 = threading.Thread(target=receive_Messages, args=[client])
        thread2 = threading.Thread(target=sendMessages, args=[client, nome, origem, destino])

        thread1.start()
        thread2.start()



main()
