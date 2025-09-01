import socket

def inicia_servidor_UDP():
    host = '127.0.0.1'
    porta = 12345

    
    try:
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_servidor.bind((host, porta))

        print(f"Servidor iniciado em: {host}:{porta}")
        print(f"Aguardando conexão com um cliente")

        while True:
            try:
                dados, endereco_cliente = socket_servidor.recvfrom(1024)
                print(f"Conexão estabelecida com {endereco_cliente}")

                mensagem = dados.decode()
                print(f"Recebido de {endereco_cliente}: {mensagem}")

                if mensagem.lower() == "sair":
                    print("Encerrando servidor UDP")
                    break

                resposta = "Mensagem recebida pelo servidor"
                socket_servidor.sendto(resposta.encode(), endereco_cliente)

            except UnicodeDecodeError:
                print("Erro ao decodificar mensagem.")
            except socket.error as e:
                print(f"Erro de socket: {e}")
                break

    
    except Exception as e:
        print(f"Erro ao iniciar o servidor UDP: {e}")

    finally:
        socket_servidor.close()
        print("Socket do servidor fechado")

if __name__ == "__main__":
    inicia_servidor_UDP()