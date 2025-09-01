import socket


def inicia_cliente_UDP():
    host = '127.0.0.1'
    porta = 12345

    try:

        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Conectando no servidor em: {host}:{porta}")
        print(f"\tSocket UDP/IPv4 criado: {socket_cliente}")
        print("\nDigite 'sair' para encerrar.")

        while True:
            try:
                mensagem = input("Você: ")
                socket_cliente.sendto(mensagem.encode(), (host, porta))

                if mensagem.lower() == "sair":
                    print("Você saiu da conversa")
                    break

                resposta, _ = socket_cliente.recvfrom(1024)
                print(f"Resposta do Servidor: {resposta.decode()}")
            
            except UnicodeEncodeError:
                print("Erro ao codificar mensagem.")
            except socket.error as e:
                print(f"Erro de comunicação: {e}")
                break

    
    except Exception as e:
        print(f"Erro ao iniciar cliente UDP: {e}")

    finally:
        socket_cliente.close()
        print("Socket fechado")
        print("Conexão fechada")

if __name__ == "__main__":
    inicia_cliente_UDP()