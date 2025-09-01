
#Processo de Criação de um Socket TCP/IP em comunicação Cliente - Servidor:
#Criação do Socket indicando a família/domínio: UNIX, INTERNET
#Tipo: stream, datagrama
#Protocolo: TCP, UDP

#Na Função:
#AF_INET se refere a INTERNET - consiste nos endereços de rede da máquina e da identificação do número da porta
#AF_UNIX se refere a UNIX - Os processos se comunicam referenciando um nome de pasta (pathname), dentro do espaço de nomes do sistema de arquivos
#Tipos de Sockets:
#Socket Stream - se refere ao protocolo TCP - provê sequenciamento e fluxo bidirecional. Transmite dados com criptografia
#Socket DGRAM - se refere ao protocolo UDP - Suporta fluxo de dados bidirecional mas não oferece o mesmo serviço confiável que o Socket Stream

#Fluxo Servidor:
# cria o socket - socket()
# liga o socket a um host e uma porta - bind()
# declara que pode receber n conexões enfileiradas - listen()
# quando houver pedido de conexão, aceita - accept()
# após o cliente enviar uma mensagem com send(), recebe a solicitação - recv()
# a partir da primeira solicitação o servidor irá responder de acordo - send()
# após toda a troca de mensagens fecha a conexão e o socket - close()

#Fluxo Cliente:
# Cria um socket idêntico ao servidor - socket()
# Pede uma conexão com o servidor e aguarda informando o mesmo host e porta - connect()
# Envia uma sequência de bytes (mensagem) pela conexão - send()
# após o envio da mensagem fica esperando uma resposta do servidor - recv()
# após toda a troca de mensagens fecha a conexão e o socket - close()

import socket


def inicia_cliente_TCP():
    host = '127.0.0.1'
    porta = 12345

    try:
        #Cria o socket do cliente
        print("\nCriando um Socket")
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"\tSocket TCP/IPv4 criado: {socket_cliente}")

        #Conexão com o servidor
        print(f"Conectando no servidor em: {host}:{porta}")
        socket_cliente.connect((host, porta)) #é uma tupla
        print("Conectado ao servidor")

        #Enviando uma mensagem
        mensagem = "Olá Servidor"
        print(f"Enviando Mensagem: {mensagem}")
        socket_cliente.send(mensagem.encode())

        #Recebe uma resposta
        resposta = socket_cliente.recv(1024)
        print(f"Resposta do Servidor: {resposta.decode()}")

    except ConnectionRefusedError as e:
        print(f"Conexão falhou")

    except Exception as e:
        print(f"um erro ocorreu: {e}")
    finally:
        #Fechando o socket
        socket_cliente.close()
        print("Socket fechado")
        print("Conexão fechada")

if __name__ == "__main__":
    inicia_cliente_TCP()