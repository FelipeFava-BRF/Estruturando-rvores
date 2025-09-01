import socket
from datetime import datetime



def chat_cliente():
    host = '127.0.0.1'
    porta = 12345

    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect((host, porta))
    print("Conectado ao Servidor. Digite 'sair' para encerrar")
    try:
        while True:
            try:
                mensagem = input("Você: ")
                socket_cliente.send(mensagem.encode())

                if mensagem.lower() == "sair":
                    print("Você encerrou a conversa")
                    break

                resposta = socket_cliente.recv(1024).decode()
                if resposta.lower() == "sair":
                    print("Servidor encerrou a conversa")
                    break
                print(f"Servidor: {resposta}")
            
            except UnicodeEncodeError:
                print("Erro ao codificar mensagem. Use apenas caracteres válidos")
            except socket.error as e:
                print(f"Erro de comunicação com o servidor: {e}")
                break

    except socket.gaierror:
        print("Erro de endereço. Verifique o IP ou hostname.")
    except ConnectionRefusedError:
        print("Servidor não está disponível ou recusou a conexão.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        socket_cliente.close()
        print("Conexão encerrada")

if __name__ == "__main__":
    chat_cliente()