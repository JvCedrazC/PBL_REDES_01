# Relatório Técnico: Sistema de Reservas de Passagens Aéreas
## Introdução
Este relatório descreve a implementação de um sistema de reservas de passagens aéreas para uma companhia de baixo custo. O sistema permite que os clientes consultem e reservem assentos em rotas entre cidades conectadas. A comunicação é realizada entre os clientes e um servidor central por meio de uma rede TCP/IP utilizando a API Socket.

## Estrutura do Sistema
O sistema consiste em duas partes principais:
* Servidor: Centraliza o controle das rotas, calcula os caminhos disponíveis entre as cidades e gerencia as reservas de assentos.
* Clientes: Enviam pedidos ao servidor para consultar rotas e reservar passagens, recebendo as respostas em tempo real.
### Códigos cliente e servidor
* Código do servidor:
 ```ruby
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
  
  def communication(socket_client):
      try:
          while True:
              msg = socket_client.recv(8192)
              if not msg:
                  break  # Se não houver mensagem, o cliente se desconectou

            data = pickle.loads(msg)
            source, target, type_of_request = data[0], data[1], data[2]
            print(f'Source: {source}, Target: {target}, Type of request: {type_of_request}')

            if type_of_request == 0:
                with clients_lock:
                    if socket_client in list_clients:
                        print('Calculando rotas...')
                        all_paths = find_path(graph, source, target)
                        all_paths = [path for path in all_paths if len(path) <= 4]  # Filtra rotas com mais de 4 cidades
                        print('Rotas calculadas:', all_paths)

                        rotes_tickets = generate_tickets(all_paths)

                        # Limita as rotas enviadas a 3
                        msg_to_client = pickle.dumps(rotes_tickets)
                        print('Enviando Rotas...')
                        socket_client.sendall(msg_to_client)
                        print('Rotas enviadas!')
                    else:
                        print('Cliente desconectado')
            else:
                socket_client.sendall(pickle.dumps('Mensagem teste!'))
    except Exception as e:
        print(f'Erro na comunicação: {e}')
    finally:
        with clients_lock:
            list_clients.remove(socket_client)  # Remove cliente desconectado
        socket_client.close()

  def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('172.16.103.222', 777))
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

  ```
* Código do Cliente
  ```ruby
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
  ```

## Funcionalidades do Sistema
* Consulta de Rotas: O cliente pode solicitar as rotas disponíveis entre duas cidades. O servidor calcula todas as rotas possíveis com no máximo quatro conexões entre cidades.
* Reserva de Passagens: Após a consulta, o cliente pode selecionar um ou mais trechos e reservar os assentos disponíveis. O sistema garante que o cliente que iniciar a compra primeiro terá preferência sobre os demais.
* Gestão de Concorrência: O sistema suporta múltiplos clientes simultaneamente, e usa mecanismos de sincronização para evitar conflitos nas reservas de assentos.
## Implementação
### Comunicação em Rede (TCP/IP)
* O sistema utiliza sockets TCP para garantir a integridade e confiabilidade das conexões entre os clientes e o servidor. O uso do protocolo TCP é justificado pela necessidade de garantir que todas as mensagens sejam entregues corretamente, sem perda de pacotes ou reordenação, o que é crucial em um sistema de reservas de assentos.

### API Socket
* A API de comunicação foi implementada em Python utilizando a biblioteca socket. Cada cliente se conecta ao servidor e envia suas solicitações em formato serializado (pickle), permitindo a transmissão de dados complexos (listas e dicionários) de forma simples. O servidor processa essas mensagens e responde com os resultados solicitados.

### Protocolo de Comunicação
* Foi definido um protocolo simples para o envio de mensagens entre cliente e servidor:

 * Mensagem Cliente -> Servidor: (origem, destino, tipo_de_requisicao)
   * origem: Cidade de origem do cliente.
   * destino: Cidade de destino desejada.
   * tipo_de_requisicao: 0 para consulta de rotas e 1 para reserva de assentos.
* Mensagem Servidor -> Cliente:
  * Para consultas, o servidor responde com um dicionário contendo as rotas disponíveis e o número de assentos restantes em cada trecho.
  * Para reservas, o servidor confirma se a reserva foi bem-sucedida ou informa que os assentos foram esgotados.
 * Estrutura de Dados
   * O servidor utiliza a biblioteca networkx para criar e gerenciar um grafo não direcionado representando as cidades e as conexões entre elas. Este grafo é carregado a partir de um arquivo de texto (cidades.txt), onde cada linha representa uma conexão entre duas cidades.
   * A função find_path calcula todas as rotas possíveis entre duas cidades usando o grafo, com um limite de até quatro conexões. Isso evita que o cliente precise fazer muitas trocas de voos, garantindo que as rotas oferecidas sejam viáveis.

### Arquitetura do servidor
A arquitetura que melhor descreve o servidor é a arquitetura statefull, e, apesar de não haver persistência de dados, o contexto de cada transação fica salvo e cada thread executada pode ser retomada para o estado anterior em caso de erros. O servidor também permite armazenar o estado das rotas que é compartilhado com diferentes clientes. Este estado fica salvo na variável global route_tickets e a informação do estado das rotas persiste durante a execução do servidor.

### Concorrência e Sincronização
Para suportar múltiplos clientes simultaneamente, o servidor utiliza threads. Cada cliente conectado é atendido em uma thread separada, permitindo que vários clientes façam consultas e reservas ao mesmo tempo.
No entanto, para evitar que dois clientes reservem o mesmo assento ao mesmo tempo, foi implementado um mecanismo de locks. Um lock exclusivo garante que apenas um cliente por vez possa interagir com os dados de uma rota, evitando condições de corrida.

### Alocação de Assentos
Ao calcular as rotas, o servidor gera aleatoriamente o número de assentos disponíveis para cada trecho, entre 0 e 6. Isso simula a variação no número de lugares disponíveis em diferentes voos. Quando um cliente solicita a reserva, o servidor reduz o número de assentos restantes.
Se um cliente não concluir a compra em um tempo limite, a reserva é cancelada, e os assentos são liberados para outros clientes.

## Considerações Finais
### Escolhas Técnicas
* Threads e Locks: O uso de threads permite que o sistema atenda vários clientes ao mesmo tempo, e a sincronização com locks evita conflitos na reserva de assentos.
* Limitação de Conexões (Máximo de 4 Cidades): Para melhorar a experiência do usuário e evitar sobrecarga no cálculo de rotas, o sistema limita as rotas a no máximo quatro conexões entre cidades.
### Possíveis Melhorias Futuras
* Persistência de Dados: Atualmente, o sistema gera os dados de assentos aleatoriamente a cada consulta. Uma melhoria seria adicionar um banco de dados para armazenar persistentemente as reservas de assentos.
* Validação de Timeout para Reservas: Implementar um sistema de timeout mais sofisticado para garantir que reservas expiradas sejam liberadas de forma automática, evitando assentos bloqueados por muito tempo.
## Conclusão
O sistema de reservas desenvolvido oferece uma solução robusta para a gestão de passagens aéreas, utilizando comunicação baseada em TCP/IP para garantir uma interação eficiente entre clientes e servidor. A gestão de concorrência e a alocação de recursos (assentos) foram cuidadosamente planejadas para garantir que o cliente que fizer a reserva primeiro tenha prioridade, evitando conflitos.

Essa implementação pode ser expandida para incluir funcionalidades adicionais e melhorar a persistência e escalabilidade do sistema.
