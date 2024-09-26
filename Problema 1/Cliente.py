import socket
import pickle

def citys(number):
    # Supondo que você tenha uma função que retorna a cidade com base no número
    cities = {
        1: "Barreiras",
        2: "Salvador",
        3: "Fortaleza",
        4: "Brasilia",
        5: "Patos",
        6: "Terezina",
        7: "Vitoria",
        8: "Uberlandia",
        9: "Recife",
        10: "Manaus"
    }
    return cities.get(number, "Cidade inválida")

def buy_rotes(buy, msg):
    contador = 0
    rota_escolhida = None
    for rota, passagem in msg.items():
        if contador == buy:
            if passagem > 0:
                msg[rota] -= 1  # Decrementa o número de passagens
                rota_escolhida = rota
            else:
                print("Passagens esgotadas para essa rota.")
            break
        contador += 1
    return rota_escolhida, msg  # Retorna a rota escolhida e o dicionário atualizado


def main():

    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(('localhost', 777))
    print('Conectado')

    sair = 0
    s = 0

    print("-------- Bem vindo ao VendPass --------\n")

    while sair == 0:
        request = []
        try:
            print("Escolha o número que represente o seu local de origem (local de onde você quer viajar)\n 1 = Barreiras(BA)\n 2 = Salvador(BA)\n 3 = Fortaleza(CE) \n 4 = Brasilia(DF)\n 5 = Patos(PB)\n 6 = Terezina(PI)\n 7 = Vitoria(ES)\n 8 = Uberlandia(MG)\n 9 = Recife(PE)\n 10 = Manaus(AM)\n 11 = Para sair")
            source = int(input("Origem: "))
            if source == 11:
                break

            print("Escolha o número que represente o seu local de destino (local para onde você quer viajar)\n 1 = Barreiras(BA)\n 2 = Salvador(BA)\n 3 = Fortaleza(CE) \n 4 = Brasilia(DF)\n 5 = Patos(PB)\n 6 = Terezina(PI)\n 7 = Vitoria(ES)\n 8 = Uberlandia(MG)\n 9 = Recife(PE)\n 10 = Manaus(AM)\n 11 = Para sair")
            target = int(input('Destino: '))
            if target == 11:
                break
            

            source = citys(source)
            target = citys(target)
        except ValueError:
            print("Entrada inválida. Por favor, insira um número entre 1 e 11.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")




        request.extend([source, target, s])


        print("\nEnviando requisição ao servidor...")
        msg_to_server = pickle.dumps(request)
        socket_client.sendall(msg_to_server)
        print('Requisição enviada...\n')




        try:
            # Recebe as rotas do servidor
            msg = pickle.loads(socket_client.recv(4096))
            contador = 0
            print("Rotas para compra:")
            for rota, passagem in msg.items():
                print(f'Rota {contador}: {rota}. Passagens disponíveis: {passagem}')
                contador += 1
        except (pickle.UnpicklingError, EOFError) as e:
            print("Erro ao receber ou processar os dados:", e)
            continue
        except Exception as e:
            print("Ocorreu um erro inesperado ao receber dados:", e)
            continue

        try:
            # Comprar rota
            buy = int(input("Qual rota deseja comprar [0/1/2]? "))
            while buy < 0 or buy > 2:
                print("Escolha um número válido")
                buy = int(input("Qual rota deseja comprar [0/1/2]? "))
            rota_escolhida, msg_atualizado = buy_rotes(buy, msg)
            if rota_escolhida:
                print(f"Rota escolhida: {rota_escolhida}")
                # Envia o dicionário atualizado de volta para o servidor
                socket_client.sendall(pickle.dumps(msg_atualizado))
                print("Atualização de passagens enviada ao servidor.\n")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.\n")
            continue
        except Exception as e:
            print("Ocorreu um erro inesperado ao processar a compra:", e)
            continue

        continuar = input('Deseja fazer outra pesquisa [S/N]? ').upper()
        if continuar == "N":
            print('Conexão encerrada. Obrigado pela visita.')
            socket_client.close()
            break


if __name__ == "__main__":
    main()
