import socket

def chat_servidor():
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
    
    socket_cliente, endereco_cliente = socket_servidor.accept()
    print(f"Conexão estabelecida com {endereco_cliente}")
    
    try:
        while True:
            try:
                mensagem = socket_cliente.recv(1024).decode()
                if mensagem.lower() == "sair":
                    print("Cliente encerrou a conversa")
                    break
                print(f"Cliente: {mensagem}")

                resposta = input("Servidor: ")
                socket_cliente.send(resposta.encode())
                if resposta.lower() == "sair":
                    print("Servidor encerrou a conversa")
                    break
            
            except UnicodeDecodeError:
                print("Erro ao decodificar a mensagem recebida.")
            except socket.error as e:
                print(f"Erro de comunicação com o cliente: {e}")
                break

    except socket.error as e:
        print("Erro ao iniciar o servidor: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        socket_cliente.close()
        socket_servidor.close()
        print("Conexões encerradas")

if __name__ == "__main__":
    chat_servidor()