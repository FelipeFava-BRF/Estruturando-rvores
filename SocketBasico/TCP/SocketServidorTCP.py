import socket

def inicia_servidor_TCP():
    host = '127.0.0.1'
    porta = 12345

    #Cria o socket do servidor
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Ligação do socket com um host e porta
    socket_servidor.bind((host, porta)) #é uma tupla

    #Escutando conexões
    socket_servidor.listen(2)

    print(f"Servidor iniciado em: {host}:{porta}")
    print(f"Aguardando conexão com um cliente")
    
    try:
        #Aceitando conexão
        socket_cliente, endereco_cliente = socket_servidor.accept()
        print(f"Conexão estabelecida com {endereco_cliente}")

        #Recebendo dados do cliente
        dado = socket_cliente.recv(1024) #recebe até 1024 bytes
        print(f"Mensagem recebida: {dado.decode()}")

        #Enviando resposta ao cliente
        resposta = "Mensagem recebida pelo servidor"
        socket_cliente.send(resposta.encode())

        #Fecha a conexão com cliente
        socket_cliente.close()

    except KeyboardInterrupt:
        print("Servidor desligando")
    finally:
        #Fecha socket do servidor
        socket_servidor.close()
        print("Socket do servidor fechado")

if __name__ == "__main__":
    inicia_servidor_TCP()
